CREATE TABLE IF NOT EXISTS `job_tittle` (
	`id_positions` integer primary key NOT NULL UNIQUE,
	`title` TEXT NOT NULL,
FOREIGN KEY(`id_positions`) REFERENCES `employees`(`id_position_emp`)
);
CREATE TABLE IF NOT EXISTS `employees` (
	`id_employee` integer primary key NOT NULL UNIQUE,
	`fullname` TEXT NOT NULL,
	`name` TEXT NOT NULL,
	`number_phone` TEXT NOT NULL,
	`id_position_emp` INTEGER NOT NULL,
FOREIGN KEY(`id_employee`) REFERENCES `order`(`id_employee_or`)
);
CREATE TABLE IF NOT EXISTS `order` (
	`id_order` integer primary key NOT NULL UNIQUE,
	`id_client` INTEGER NOT NULL,
	`id_employee_or` INTEGER NOT NULL,
	`sum_order` INTEGER NOT NULL,
	`data_complited` TEXT NOT NULL,
	`mark_about_completed` INTEGER NOT NULL,
FOREIGN KEY(`id_client`) REFERENCES `clients`(`id_client`)
);
CREATE TABLE IF NOT EXISTS `clients` (
	`id_client` integer primary key NOT NULL UNIQUE,
	`organization` TEXT NOT NULL,
	`number_phone_client` INTEGER NOT NULL
);