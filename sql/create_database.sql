-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pokertracker
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pokertracker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pokertracker` DEFAULT CHARACTER SET utf8 ;
USE `pokertracker` ;

-- -----------------------------------------------------
-- Table `pokertracker`.`Session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Session` (
  `session_id` INT NOT NULL AUTO_INCREMENT,
  `sessioncode` VARCHAR(45) NOT NULL,
  `clientversion` VARCHAR(45) NULL,
  `mode` VARCHAR(45) NULL,
  `gametype` VARCHAR(45) NULL,
  `tablename` VARCHAR(45) NULL,
  `smallblind` DECIMAL(10,2) NULL,
  `bigblind` DECIMAL(10,2) NULL,
  `duration` TIME NULL,
  `gamecount` INT NULL,
  `startdate` TIMESTAMP NULL,
  `currency` VARCHAR(45) NULL,
  `nickname` VARCHAR(45) NULL,
  `bets` DECIMAL(10,2) NULL,
  `wins` DECIMAL(10,2) NULL,
  `chipsin` DECIMAL(10,2) NULL,
  `chipsout` DECIMAL(10,2) NULL,
  `tablesize` INT NULL,
  PRIMARY KEY (`session_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`Hand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Hand` (
  `hand_id` INT NOT NULL AUTO_INCREMENT,
  `gamecode` VARCHAR(45) NOT NULL,
  `session_id` INT NOT NULL,
  `startdate` TIMESTAMP NOT NULL,
  `profit` DECIMAL(10,2) NULL,
  `showdown` TINYINT NULL,
  PRIMARY KEY (`hand_id`),
  INDEX `fk_Hand_Session_idx` (`session_id` ASC) VISIBLE,
  INDEX `idx_hand_startdate_handid` (`startdate` ASC, `hand_id` ASC) VISIBLE,
  CONSTRAINT `fk_Hand_Session`
    FOREIGN KEY (`session_id`)
    REFERENCES `pokertracker`.`Session` (`session_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`Player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Player` (
  `player_id` INT NOT NULL AUTO_INCREMENT,
  `hand_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `seat` INT NOT NULL,
  `chips` DECIMAL(10,2) NULL,
  `bet` DECIMAL(10,2) NULL,
  `win` DECIMAL(10,2) NULL,
  `rakeamount` DECIMAL(10,2) NULL,
  `dealer` TINYINT NULL,
  `card1` CHAR(2) NULL,
  `card2` CHAR(2) NULL,
  PRIMARY KEY (`player_id`),
  INDEX `fk_Player_Hand1_idx` (`hand_id` ASC) VISIBLE,
  CONSTRAINT `fk_Player_Hand1`
    FOREIGN KEY (`hand_id`)
    REFERENCES `pokertracker`.`Hand` (`hand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`Round`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Round` (
  `round_id` INT NOT NULL AUTO_INCREMENT,
  `hand_id` INT NOT NULL,
  `roundnumber` INT NOT NULL,
  PRIMARY KEY (`round_id`),
  INDEX `fk_Round_Hand1_idx` (`hand_id` ASC) VISIBLE,
  CONSTRAINT `fk_Round_Hand1`
    FOREIGN KEY (`hand_id`)
    REFERENCES `pokertracker`.`Hand` (`hand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`ActionType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`ActionType` (
  `actiontype_id` INT NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`actiontype_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`Action`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Action` (
  `action_id` INT NOT NULL AUTO_INCREMENT,
  `round_id` INT NOT NULL,
  `amount` DECIMAL(10,2) NULL,
  `actionorder` INT NULL,
  `actiontype_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  PRIMARY KEY (`action_id`),
  INDEX `fk_Action_Round1_idx` (`round_id` ASC) VISIBLE,
  INDEX `fk_Action_ActionType1_idx` (`actiontype_id` ASC) VISIBLE,
  INDEX `fk_Action_Player1_idx` (`player_id` ASC) VISIBLE,
  CONSTRAINT `fk_Action_Round1`
    FOREIGN KEY (`round_id`)
    REFERENCES `pokertracker`.`Round` (`round_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Action_ActionType1`
    FOREIGN KEY (`actiontype_id`)
    REFERENCES `pokertracker`.`ActionType` (`actiontype_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Action_Player1`
    FOREIGN KEY (`player_id`)
    REFERENCES `pokertracker`.`Player` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`Board`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Board` (
  `board_id` INT NOT NULL AUTO_INCREMENT,
  `hand_id` INT NOT NULL,
  `boardnumber` INT NOT NULL,
  `flop` CHAR(6) NULL,
  `turn` CHAR(2) NULL,
  `river` CHAR(2) NULL,
  PRIMARY KEY (`board_id`),
  INDEX `fk_Board_Hand1_idx` (`hand_id` ASC) VISIBLE,
  CONSTRAINT `fk_Board_Hand1`
    FOREIGN KEY (`hand_id`)
    REFERENCES `pokertracker`.`Hand` (`hand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`Tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`Tag` (
  `tag_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tag_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokertracker`.`HandTag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokertracker`.`HandTag` (
  `handtag_id` INT NOT NULL AUTO_INCREMENT,
  `tag_id` INT NOT NULL,
  `hand_id` INT NOT NULL,
  PRIMARY KEY (`handtag_id`),
  INDEX `fk_HandTag_Tag1_idx` (`tag_id` ASC) VISIBLE,
  INDEX `fk_HandTag_Hand1_idx` (`hand_id` ASC) VISIBLE,
  UNIQUE INDEX `hand_id_UNIQUE` (`hand_id` ASC, `tag_id` ASC) INVISIBLE,
  CONSTRAINT `fk_HandTag_Tag1`
    FOREIGN KEY (`tag_id`)
    REFERENCES `pokertracker`.`Tag` (`tag_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_HandTag_Hand1`
    FOREIGN KEY (`hand_id`)
    REFERENCES `pokertracker`.`Hand` (`hand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `pokertracker`.`ActionType`
-- -----------------------------------------------------
START TRANSACTION;
USE `pokertracker`;
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (0, 'Fold');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (1, 'Small Blind');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (2, 'Big Blind');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (3, 'Call');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (4, 'Check');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (5, 'Bet');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (7, 'All-in');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (15, 'Ante');
INSERT INTO `pokertracker`.`ActionType` (`actiontype_id`, `description`) VALUES (23, 'Raise');

COMMIT;


-- -----------------------------------------------------
-- Data for table `pokertracker`.`Tag`
-- -----------------------------------------------------
START TRANSACTION;
USE `pokertracker`;
INSERT INTO `pokertracker`.`Tag` (`tag_id`, `name`) VALUES (1, 'favourite');

COMMIT;

