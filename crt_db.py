#!/usr/bin/env python3

import mysql.connector
import db_config

if __name__ == '__main__':
    db = mysql.connector.connect(**db_config.db)
    cursor = db.cursor()

    sql_arr = ['''
CREATE TABLE `session` (
    `id` INT NOT NULL AUTO_INCREMENT ,
    `id_user` INT NOT NULL ,
    `ip` TEXT NOT NULL ,
    `agent` TEXT NOT NULL ,
    `hash` VARCHAR(64) NOT NULL ,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;
    ''','''
ALTER TABLE `session`
ADD CONSTRAINT `fk_user`
FOREIGN KEY (`id_user`)
REFERENCES `dovidnyuk_students`(`id_student`)
ON DELETE CASCADE ON UPDATE CASCADE;
    ''','''
ALTER TABLE `dovidnyuk_students`
CHANGE `password`
`password` VARCHAR(64) NOT NULL;
    ''','''
ALTER TABLE `dovidnyuk_students` DROP INDEX `password_UNIQUE`;
    ''','''
CREATE VIEW `v_students_mark` AS
    SELECT
        `dovidnyuk_student_marks`.`PK_student_mark` AS `PK_student_mark`,
        `dovidnyuk_students`.`id_student` AS `id_student`,
        `dovidnyuk_marks`.`digital_name` AS `digital_name`,
        `dovidnyuk_group_load`.`FK_discipline` AS `FK_discipline`,
        `dovidnyuk_zaniat`.`tema_zaniattya` AS `tema_zaniattya`,
        `dovidnyuk_vudiv_zaniat`.`compact_name_vudy` AS `compact_name_vudy`
    FROM
        (((((`dovidnyuk_student_marks`
        LEFT JOIN `dovidnyuk_marks` ON ((`dovidnyuk_student_marks`.`FK_mark` = `dovidnyuk_marks`.`PK_mark`)))
        LEFT JOIN `dovidnyuk_students` ON ((`dovidnyuk_student_marks`.`FK_student` = `dovidnyuk_students`.`id_student`)))
        LEFT JOIN `dovidnyuk_zaniat` ON ((`dovidnyuk_student_marks`.`FK_zaniattya` = `dovidnyuk_zaniat`.`PK_zaniattya`)))
        LEFT JOIN `dovidnyuk_group_load` ON ((`dovidnyuk_zaniat`.`FK_load` = `dovidnyuk_group_load`.`PK_load`)))
        LEFT JOIN `dovidnyuk_vudiv_zaniat` ON ((`dovidnyuk_zaniat`.`FK_vudy_zaniattya` = `dovidnyuk_vudiv_zaniat`.`id_vudy_zaniattya`)));
    ''','''
CREATE VIEW `v_stundent_lesson` AS
    SELECT
        `dovidnyuk_students`.`id_student` AS `id_student`,
        `dovidnyuk_group_load`.`FK_discipline` AS `FK_discipline`,
        `dovidnyuk_discipline`.`discipline_name` AS `discipline_name`
    FROM
        ((`dovidnyuk_group_load`
        JOIN `dovidnyuk_students` ON ((`dovidnyuk_students`.`fk_group` = `dovidnyuk_group_load`.`FK_group`)))
        JOIN `dovidnyuk_discipline` ON ((`dovidnyuk_discipline`.`PK_discipline` = `dovidnyuk_group_load`.`FK_discipline`)));
    ''']

    msg_arr = ["Session was added", "FK for session was added",
    "Pass was expanded", "Pass was made not unique",
    "View 0 created", "View 1 created"]

    print("Starting...")

    try:
        for i in range(0, len(sql_arr)):
                cursor.execute(sql_arr[i])
                print(msg_arr[i], '[{}/{}]'.format(i+1, len(sql_arr)))
                db.commit()
    except mysql.connector.errors.ProgrammingError:
        print('DB are already created')
    db.close()
