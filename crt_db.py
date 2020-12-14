#!/usr/bin/env python3

import mysql.connector
import db_config

if __name__ == '__main__':
    db = mysql.connector.connect(**db_config.db)
    cursor = db.cursor()

    sql_for_session = '''
CREATE TABLE `session` (
    `id` INT NOT NULL AUTO_INCREMENT ,
    `id_user` INT NOT NULL ,
    `ip` TEXT NOT NULL ,
    `agent` TEXT NOT NULL ,
    `hash` VARCHAR(64) NOT NULL ,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;
    '''

    sql_for_fk = '''
ALTER TABLE `session`
ADD CONSTRAINT `fk_user`
FOREIGN KEY (`id_user`)
REFERENCES `dovidnyuk_students`(`id_student`)
ON DELETE CASCADE ON UPDATE CASCADE;
    '''

    sql_for_pass_expand = '''
ALTER TABLE `dovidnyuk_students`
CHANGE `password`
`password` VARCHAR(64) NOT NULL;
    '''

    sql_for_pass_not_uq = '''
ALTER TABLE `dovidnyuk_students` DROP INDEX `password_UNIQUE`;
    '''

    print("Starting...")
    cursor.execute(sql_for_session)
    db.commit()
    print("Session was added")
    cursor.execute(sql_for_fk)
    db.commit()
    print("FK for session was added")
    cursor.execute(sql_for_pass_expand)
    db.commit()
    print("Pass was expanded")
    cursor.execute(sql_for_pass_not_uq)
    db.commit()
    print("Pass was made not unique")
    db.close()
