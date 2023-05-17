! Read and check inputs
CALL READ_MISC
REWIND(LUINPUT); CALL READ_INPUTS
REWIND(LUINPUT); CALL READ_OUTPUTS
REWIND(LUINPUT); CALL READ_COMPUTATIONAL_DOMAIN
REWIND(LUINPUT); CALL READ_TIME_CONTROL
REWIND(LUINPUT); CALL READ_SIMULATOR
REWIND(LUINPUT); CALL READ_CALIBRATION
REWIND(LUINPUT); CALL READ_SUPPRESSION
REWIND(LUINPUT); CALL READ_SPOTTING
REWIND(LUINPUT); CALL READ_SMOKE
REWIND(LUINPUT); CALL READ_MONTE_CARLO ; NUM_ENSEMBLE_MEMBERS0 = NUM_ENSEMBLE_MEMBERS
CLOSE(LUINPUT)
CALL READ_FUEL_MODEL_TABLE
CALL READ_CALIBRATION_BY_PYROME

IF (IRANK_WORLD .EQ. 0) THEN
   CALL CHECK_INPUTS(GOOD_INPUTS)
   IF (.NOT. GOOD_INPUTS) CALL SHUTDOWN()
ENDIF

! Initialize random number generator - this has to be done after inputs are read in
! because both SEED and RANDOMIZE_RANDOM_SEED are user-specified
CALL RANDOM_SEED(SIZE=M)
ALLOCATE(K(M))

IF (RANDOMIZE_RANDOM_SEED) THEN
   K(:) = (IT1/1000) * (IRANK_WORLD+1) * (/ (I, I = 1, M) /) !IT1 is from earlier call to SYSTEM_CLOCK
ELSE
   K(:) = SEED !+ IRANK_WORLD
ENDIF
CALL RANDOM_SEED(PUT=K(1:M))

CALL SUNRISE_SUNSET_CALCS (LONGITUDE, LATITUDE, UTC_OFFSET_HOURS, CURRENT_YEAR, HOUR_OF_YEAR)

CALL MPI_BARRIER(MPI_COMM_WORLD, IERR)
CALL ACCUMULATE_CPU_USAGE(2, IT1, IT2)

! Build lookup tables for trigonometric arrays, wind adjustment factor, nonburnable mask, etc.
CALL INIT_LOOKUP_TABLES

CALL SETUP_PARALLEL_IO

IF (IRANK_WORLD .EQ. 0 .AND. DUMP_PROGRESS_MESSAGES) THEN
   MESSAGESTR='ELMFIRE is reading fuel and weather data'
   CALL WRITE_PROGRESS_MESSAGE(MESSAGESTR)
ENDIF

IF (IRANK_WORLD .EQ. 0) WRITE(*,*) 'Reading headers for fuels/topography and weather rasters'

IF (USE_TILED_IO) THEN
   IF (IRANK_WORLD .EQ. PARALLEL_IO_RANK(1)) THEN
      FN = TRIM(FUELS_AND_TOPOGRAPHY_DIRECTORY) // TRIM(ASP_FILENAME)
      CALL READ_BSQ_HEADER_EXISTING_TILED (ASP,FN)
   ENDIF
   IF (IRANK_WORLD .EQ. PARALLEL_IO_RANK(2)) THEN
      FN = TRIM(WEATHER_DIRECTORY) // TRIM(WS_FILENAME)
      CALL READ_BSQ_HEADER_EXISTING_TILED (WS,FN)
   ENDIF
ELSE
   IF (IRANK_WORLD .EQ. PARALLEL_IO_RANK(1)) THEN
      CALL READ_BSQ_HEADER (ASP, FUELS_AND_TOPOGRAPHY_DIRECTORY, ASP_FILENAME, .FALSE.)
   ENDIF

   IF (IRANK_WORLD .EQ. PARALLEL_IO_RANK(2)) THEN
      CALL READ_BSQ_HEADER (WS , WEATHER_DIRECTORY             , WS_FILENAME , .FALSE.)
   ENDIF
ENDIF

IF (NPROC .GT. 1) THEN
   CALL MPI_BCAST_RASTER_HEADER(ASP, PARALLEL_IO_RANK(1), .TRUE.)
   CALL MPI_BCAST_RASTER_HEADER(WS , PARALLEL_IO_RANK(2), .TRUE.)
ENDIF

CALL ACCUMULATE_CPU_USAGE(3, IT1, IT2)

IF (IRANK_WORLD .EQ. 0) WRITE(*,*) 'Setting up shared memory, part 1'
CALL SETUP_SHARED_MEMORY_1

CALL MPI_BARRIER(MPI_COMM_WORLD, IERR)
CALL ACCUMULATE_CPU_USAGE(4, IT1, IT2)

IF (IRANK_WORLD .EQ. 0) WRITE(*,*) 'Reading weather, fuel, and topography rasters'

IF (USE_TILED_IO) THEN
   CALL READ_WEATHER_FUEL_TOPOGRAPHY_TILED
ELSE
   CALL READ_WEATHER_FUEL_TOPOGRAPHY
ENDIF

CALL MPI_BARRIER(MPI_COMM_WORLD, IERR)
CALL ACCUMULATE_CPU_USAGE(5, IT1, IT2)

IF (MULTIPLE_HOSTS) CALL BCAST_WEATHER_FUEL_TOPOGRAPHY

IF (ABS(GRID_DECLINATION) .GT. 0.1 ) THEN
   IF (ROTATE_ASP) CALL ROTATE_ASP_AND_WD(1)
   IF (ROTATE_WD ) CALL ROTATE_ASP_AND_WD(2)
ENDIF

WHERE(FBFM%I2(:,:,1) .GT. 303) FBFM%I2(:,:,1) = 256
WHERE(FBFM%I2(:,:,1) .LT.   0) FBFM%I2(:,:,1) =  99

IF (USE_PYROMES .AND. ADJUSTMENT_FACTORS_BY_PYROME) THEN
   DO IY = 1, FBFM%NROWS
   DO IX = 1, FBFM%NCOLS
      IF (FBFM%I2(IX,IY,1) .LT. 101 .OR. FBFM%I2(IX,IY,1) .GT. 204) CYCLE
      IF (PYROMES%I2(IX,IY,1) .LT. 1 .OR. PYROMES%I2(IX,IY,1) .GT. 128) THEN
         ADJ%R4(IX,IY,1) = 1.0
      ELSE
         ADJ%R4(IX,IY,1) = ADJ_PYROME(PYROMES%I2(IX,IY,1),FBFM%I2(IX,IY,1))
      ENDIF
   ENDDO
   ENDDO
ENDIF

CALL MPI_BARRIER(MPI_COMM_WORLD, IERR)
CALL ACCUMULATE_CPU_USAGE(6, IT1, IT2)

! Now that weather, fuel, topography are read in map fine inputs to coarse inputs
ALLOCATE(ICOL_ANALYSIS_F2C(1:ANALYSIS_NCOLS))
ALLOCATE(IROW_ANALYSIS_F2C(1:ANALYSIS_NROWS))
CALL MAP_FINE_TO_COARSE(WS, ASP, ICOL_ANALYSIS_F2C, IROW_ANALYSIS_F2C)

! Allocate additional rasters
IF (MODE .EQ. 1 .OR. MODE .EQ. 3) THEN
   IF (IRANK_WORLD .EQ. 0) WRITE(*,*) 'Allocating additional rasters'
   R=>ASP
   IF (DUMP_EMBER_FLUX) THEN
      CALL ALLOCATE_EMPTY_RASTER(EMBER_FLUX, R%NCOLS, R%NROWS, 1, R%XLLCORNER, R%YLLCORNER, R%CELLSIZE, 0., 'SIGNEDINT ')
   ENDIF

   IF (IRANK_WORLD .GT. 0 .OR. (IRANK_WORLD .EQ. 0 .AND. NPROC .EQ. 1)) THEN
      CALL ALLOCATE_EMPTY_RASTER(ANALYSIS_SURFACE_FIRE, R%NCOLS, R%NROWS, 1, R%XLLCORNER, R%YLLCORNER, R%CELLSIZE, R%NODATA_VALUE, 'SIGNEDINT ')
   ENDIF

   ALLOCATE (WSP    (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (WDP    (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (M1P    (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (M10P   (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (M100P  (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (MLHP   (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (MLWP   (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (MFOLP  (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (ERCP   (1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
   ALLOCATE (IGNFACP(1:WS%NCOLS,1:WS%NROWS,1:NUM_METEOROLOGY_TIMES))
ENDIF

IF (IRANK_HOST .EQ. 0) CALL INIT_RASTERS

CALL MPI_BARRIER(MPI_COMM_WORLD, IERR)
CALL ACCUMULATE_CPU_USAGE(7, IT1, IT2)

IF (MODE .NE. 2) THEN
   WRITE(*,*) 'Calculating NUM_CASES_TOTAL'
   IF (CSV_FIXED_IGNITION_LOCATIONS) THEN
      CALL DETERMINE_NUM_CASES_TOTAL_CSV
   ELSE
      CALL DETERMINE_NUM_CASES_TOTAL
   ENDIF
   IF (NPROC .GT. 1) CALL MPI_BCAST(NUM_CASES_TOTAL, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, IERR)
   IF (NUM_MONTE_CARLO_VARIABLES .GT. 0) ALLOCATE(COEFFS_UNSCALED_BY_CASE(1:NUM_CASES_TOTAL,1:NUM_MONTE_CARLO_VARIABLES))
ENDIF
