DROP TABLE IF EXISTS `chats`;
CREATE TABLE `chats` (    
    `Chat_id` int(11) NOT NULL,    
    `Chat_type` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
    `Username` varchar(300) COLLATE utf8_spanish_ci,
    `Chat_title` varchar(100) COLLATE utf8_spanish_ci,    
    `Active` BOOLEAN    
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

ALTER TABLE `chats`
    ADD PRIMARY KEY (`Chat_id`);