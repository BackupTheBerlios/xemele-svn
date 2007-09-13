-- phpMyAdmin SQL Dump
-- version 2.10.0-rc1
-- http://www.phpmyadmin.net
-- 
-- Host: localhost
-- Generation Time: Sep 07, 2007 at 10:08 AM
-- Server version: 5.0.24
-- PHP Version: 5.2.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

-- 
-- Database: `xemele_bot`
-- 

-- --------------------------------------------------------

-- 
-- Table structure for table `associations`
-- 

CREATE TABLE `associations` (
  `id` int(11) NOT NULL auto_increment,
  `user_jid` varchar(255) NOT NULL,
  `app_jid` varchar(255) NOT NULL,
  `app_userid` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;
