CREATE TABLE IF NOT EXISTS `products` (
	`id_product` integer primary key NOT NULL UNIQUE,
	`name_product` TEXT NOT NULL,
	`id_category` INTEGER NOT NULL,
	`price` INTEGER NOT NULL,
	`quantity` INTEGER NOT NULL,
FOREIGN KEY(`id_product`) REFERENCES `check`(`id_product`)
);
CREATE TABLE IF NOT EXISTS `categories` (
	`id_category` integer primary key NOT NULL UNIQUE,
	`name_category` TEXT NOT NULL,
FOREIGN KEY(`id_category`) REFERENCES `products`(`id_category`)
);
CREATE TABLE IF NOT EXISTS `check` (
	`id_check` integer primary key NOT NULL,
	`date` TEXT NOT NULL,
	`id_product` INTEGER NOT NULL,
	`quantity` INTEGER NOT NULL
);