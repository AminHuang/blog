-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- 主机: w.rdc.sae.sina.com.cn:3307
-- 生成日期: 2015 年 02 月 28 日 21:33
-- 服务器版本: 5.5.23
-- PHP 版本: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `app_amintest`
--

-- --------------------------------------------------------

--
-- 表的结构 `blog`
--

CREATE TABLE IF NOT EXISTS `blog` (
  `titleId` int(11) NOT NULL AUTO_INCREMENT,
  `titleName` varchar(30) NOT NULL,
  `contentSimple` varchar(140) NOT NULL,
  `contentDetail` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`titleId`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- 转存表中的数据 `blog`
--

INSERT INTO `blog` (`titleId`, `titleName`, `contentSimple`, `contentDetail`, `date`) VALUES
(1, 'test', 'test', 'Test my first blog!', '2015-02-28 20:23:48'),
(2, 'second', 'second', 'my second', '2015-02-28 21:22:54'),
(3, 'third', 'my third blog', 'my third blog', '2015-02-28 21:31:55');
