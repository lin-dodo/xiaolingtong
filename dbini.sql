CREATE TABLE `task` (
	`id`	integer PRIMARY KEY AUTOINCREMENT,
	`username`	char(30),
	`task`	char(100),
	`send_list`	char(255),
	`set_date`	datetime,
	`send_way`	char(4),
	`status`	char(10) DEFAULT '('未发送')'
);
create table `contacts_group`(
	`id` integer primary key autoincrement,
	`group_name` char(30) primary key,
	`username` char(30)
)

