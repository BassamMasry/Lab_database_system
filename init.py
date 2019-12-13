import os

import mysql.connector
from mysql.connector import errorcode

DB_NAME= "Labs"

try:
  cnx = mysql.connector.connect(user='root',password=os.environ.get("sqlpass"),host='127.0.0.1',charset='utf8mb4')
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  else:
    print(err)

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
    print("Database already exists and in use")
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

TABLES = {}

tests = "'Alcohol, breath','Alcohol, saliva','Allergen specific IgE and/or mixed allergen panel','Amphetamines','Apolipoprotein E (APOE) gene','Barbiturates','Benzodiazepines','Beta-glucocerebrosidase (GBA)','Bilirubin, urine','BRCA mutations','Buprenorphine','Cannabinoids (THC)','Carbon Monoxide','Chloride','Cholesterol','Cocaine metabolites','Creatinine','CYP2C19 genotype','CYP2C9 genotype','CYP2D6 genotype','CYP3A5 genotype','DPYD genotype','EDDP (methadone metabolite)','Estrone-3 glucuronide','Ethanol (alcohol)','Factor II','Factor V','Fecal occult blood','Fern test, saliva','Follicle stimulating hormone (FSH)','Fructosamine','Glucose','Glucose monitoring','Glucose, fluid (approved by FDA for prescription h','Glucose, urine','Glycated hemoglobin, total','Glycosylated Hemoglobin (Hgb A1c)','hCG, serum, qualitative','hCG, Urine','HDL cholesterol','Hemoglobin','Hemoglobin A1','HIV antibodies','Ketone, blood','Ketone, urine','Lactic acid (lactate)','LDL cholesterol','LRRK2 gene','Leukocyte esterase, urinary','Luteinizing hormone (LH)','Methadone','Methadone metabolite (EDDP)','Methamphetamine/amphetamine','Methamphetamines','Methylenedioxymethamphetamine (MDMA)','Microalbumin','Morphine','MUTYH gene','Nitrite, urine','Opiates','Ovulation test (LH)','Oxycodone','pH','pH, urine','Phencyclidine (PCP)','Phenobarbital','Propoxyphene','Protein, total, urine','Semen','SERPINA1 gene','Solute carrier organic anion transporter family','TPMT genotype','Tricyclic antidepressants','Triglyceride','UGT1A1 genotype','Urinary protein, qualitative','Urine dipstick or tablet analytes, nonautomated','Urine hCG','Urine qualitative dipstick bilirubin','Urine qualitative dipstick blood','Urine qualitative dipstick creatinine','Urine qualitative dipstick glucose','Urine qualitative dipstick ketone','Urine qualitative dipstick leukocytes','Urine qualitative dipstick nitrite','Urine qualitative dipstick Ph','Urine qualitative dipstick protein','Urine qualitative dipstick urobilinogen','Urobilinogen, urine','Vaginal pH','Whole blood qualitative dipstick glucose'"


TABLES['patient_essentials'] = ("CREATE TABLE patient_essentials ("
	" code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
	" name char(80) NOT NULL,"
	" insurance bigint UNSIGNED NOT NULL DEFAULT 0 );")
	
TABLES['patient_extras'] = ("CREATE TABLE patient_extras ("
	" p_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
	" sex char(1) NOT NULL DEFAULT 'm',"
	" phone BIGINT UNSIGNED NOT NULL,"
	" bdate date,"
	" blood_type ENUM('unknown', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+', 'O-', 'O+') NOT NULL DEFAULT 'unknown',"
	" street varchar(100) NOT NULL DEFAULT '0',"
	" district ENUM('TODO'),"
	" province ENUM('TODO'),"
	" FOREIGN KEY (p_code) REFERENCES patient_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['patient_medcon'] = ("CREATE TABLE patient_medcon ("
	" p_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" con varchar(40) NOT NULL DEFAULT '0',"
	" FOREIGN KEY (p_code) REFERENCES patient_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")
	
TABLES['device_essentials'] = ("CREATE TABLE device_essentials ("
	" code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
	" serial INT UNSIGNED NOT NULL DEFAULT 0,"
	" type ENUM('TODO'),"
	" maint_date date);")

TABLES['device_extras'] = ("CREATE TABLE device_extras ("
	" d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" name varchar(50) NOT NULL DEFAULT '0',"
	" model varchar(30) NOT NULL DEFAULT '0',"
	" manufacturer ENUM('TODO') NOT NULL,"
	" country ENUM('TODO') NOT NULL,"
	" receive_date date,"
	" cost int,"
	" FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['device_description'] = ("CREATE TABLE device_description ("
	" d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" description varchar(255) NOT NULL DEFAULT '0',"
	" FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['device_datasheet'] = ("CREATE TABLE device_datasheet ("
	" d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" file_path varchar(255) NOT NULL DEFAULT '0',"
	" FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")
		
TABLES['analytics'] = ("CREATE TABLE analytics ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " name varchar(80) NOT NULL,"
    " SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    " sex char(1) NOT NULL DEFAULT 'm',"
    " bdate date,"
    " position varchar(90) NOT NULL,"
    " street varchar(100) NOT NULL DEFAULT '0',"
    " district ENUM('TODO'),"
    " province ENUM('TODO'),"
    " exp_years TINYINT UNSIGNED DEFAULT 0,"
    " salary MEDIUMINT UNSIGNED DEFAULT 2000,"
    " join_date date NOT NULL,"
    " retirement_date date);")
	
TABLES['analytic_phones'] = ("CREATE TABLE analytic_phones ("
	" a_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" phone BIGINT UNSIGNED NOT NULL,"
	" FOREIGN KEY (a_code) REFERENCES analytics(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['a_qualifications'] = ("CREATE TABLE a_qualifications ("
	" a_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" qualification varchar(255) NOT NULL,"
	" FOREIGN KEY (a_code) REFERENCES analytics(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")
	
TABLES['a_days_work'] = ("CREATE TABLE a_days_work ("
	" a_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" day ENUM('friday', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday') NOT NULL,"
	" FOREIGN KEY (a_code) REFERENCES analytics(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['a_dependent'] = ("CREATE TABLE a_dependent ("
	" dep_id smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " a_code smallint UNSIGNED NOT NULL,"
	" SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    " name varchar(80) NOT NULL,"
    " bdate date,"
    " sex char(1) NOT NULL DEFAULT 'm',"
	" FOREIGN KEY (a_code) REFERENCES analytics(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")


TABLES['other_staff'] = ("CREATE TABLE other_staff ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " name varchar(80) NOT NULL,"
    " SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    " sex char(1) NOT NULL DEFAULT 'm',"
    " bdate date,"
    " role varchar(90) NOT NULL,"
    " street varchar(100) NOT NULL DEFAULT '0',"
    " district ENUM('TODO'),"
    " province ENUM('TODO'),"
    " exp_years TINYINT UNSIGNED DEFAULT 0,"
    " salary MEDIUMINT UNSIGNED DEFAULT 2000,"
    " join_date date NOT NULL,"
    " retirement_date date);")
	
TABLES['staff_phones'] = ("CREATE TABLE staff_phones ("
	" s_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" phone BIGINT UNSIGNED NOT NULL,"
	" FOREIGN KEY (s_code) REFERENCES other_staff(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['s_qualifications'] = ("CREATE TABLE s_qualifications ("
	" s_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" qualification varchar(255) NOT NULL,"
	" FOREIGN KEY (s_code) REFERENCES other_staff(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")
	
TABLES['s_days_work'] = ("CREATE TABLE s_days_work ("
	" s_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" day ENUM('friday', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday') NOT NULL,"
	" FOREIGN KEY (s_code) REFERENCES other_staff(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['s_dependent'] = ("CREATE TABLE s_dependent ("
	" dep_id smallint UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " s_code smallint UNSIGNED NOT NULL,"
	" SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    " name varchar(80) NOT NULL,"
    " bdate date,"
    " sex char(1) NOT NULL DEFAULT 'm',"
	" FOREIGN KEY (s_code) REFERENCES other_staff(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['schedule'] = ("CREATE TABLE schedule ("
	" code smallint UNSIGNED AUTO_INCREMENT NOT NULL,"
    " a_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " p_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " date date PRIMARY KEY,"
	" FOREIGN KEY (a_code) REFERENCES analytics(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE,"
    " FOREIGN KEY (p_code) REFERENCES patient_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['sched_tests'] = ("CREATE TABLE sched_tests ("
	" sc_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
	" test ENUM(" + tests + ") PRIMARY KEY NOT NULL,"
	" FOREIGN KEY (sc_code) REFERENCES schedule(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['tests'] = ("CREATE TABLE tests ("
	" code smallint UNSIGNED NOT NULL,"
    " p_code smallint UNSIGNED NOT NULL,"
    " t_type ENUM(" + tests + ") NOT NULL,"
    " start_date date NOT NULL,"
    " cost smallint UNSIGNED NOT NULL,"
    " deliver_date date,"
    " results varchar(20) NOT NULL DEFAULT '0',"
    " UNIQUE index (p_code,t_type,start_date),"
    " FOREIGN KEY (p_code) REFERENCES patient_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['users'] = ("CREATE TABLE users ("
	" code smallint UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " username varchar(51) UNIQUE NOT NULL,"
    " hash char(32) NOT NULL,"
    " token char(32) NOT NULL,"
    " email varchar(70) NOT NULL,"
    " p_code smallint UNSIGNED NOT NULL,"
    " FOREIGN KEY (p_code) REFERENCES patient_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

TABLES['log'] = ("CREATE TABLE log ("
	" code mediumint UNSIGNED PRIMARY KEY NOT NULL,"
	" admin char(25) NOT NULL,"
    " operation ENUM('add', 'delete', 'modify') NOT NULL,"
    " date datetime NOT NULL);")


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='\n')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
