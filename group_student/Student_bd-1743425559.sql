CREATE TABLE IF NOT EXISTS `student` (
	`id_student` integer primary key NOT NULL UNIQUE,
	`id_level` INTEGER NOT NULL,
	`id_way` INTEGER NOT NULL,
	`id_type_education` INTEGER NOT NULL,
	`fullname` TEXT NOT NULL,
	`name` TEXT NOT NULL,
	`secondname` TEXT NOT NULL,
	`average_score` REAL NOT NULL,
FOREIGN KEY(`id_level`) REFERENCES `level_education`(`id_level`),
FOREIGN KEY(`id_way`) REFERENCES `way`(`id_way`),
FOREIGN KEY(`id_type_education`) REFERENCES `type_education`(`id_type`)
);
CREATE TABLE IF NOT EXISTS `level_education` (
	`id_level` integer primary key NOT NULL UNIQUE,
	`title_ed` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `way` (
	`id_way` integer primary key NOT NULL UNIQUE,
	`title_way` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `type_education` (
	`id_type` integer primary key NOT NULL UNIQUE,
	`title_type` TEXT NOT NULL
);