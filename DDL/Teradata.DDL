CREATE SET TABLE Employee_Database.Employee ,FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      Employee_Id INTEGER,
      Employee_BIGINT BIGINT,
      Employee_Name CHAR(25) CHARACTER SET LATIN NOT CASESPECIFIC,
      Salary DECIMAL(8,2),
      Salary_Num NUMERIC(8,2),
      Salary_Float Float,
      DOB DATE FORMAT 'YYYY-MM-DD',
      Job_Title VARCHAR(25) CHARACTER SET LATIN NOT CASESPECIFIC,
      Dept_No SMALLINT,
      Marital_Status CHAR(1) CHARACTER SET LATIN NOT CASESPECIFIC,
      No_Of_Dependents1 BYTEINT,
      No_Of_Dependents2 TIMESTAMP,
      No_Of_Dependents2_2 TIME,
	 No_Of_Dependents3 BYTEINT)
UNIQUE PRIMARY INDEX ( Employee_Id );