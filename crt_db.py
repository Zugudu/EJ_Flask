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

    cursor.execute(sql_for_session)
    db.commit()
    cursor.execute(sql_for_fk)
    db.commit()
    db.close()
