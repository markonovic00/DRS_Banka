-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 19, 2022 at 07:45 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `drs_banka`
--

-- --------------------------------------------------------

--
-- Table structure for table `credit_card`
--

CREATE TABLE `credit_card` (
  `card_number` varchar(30) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `pin_code` int(11) NOT NULL,
  `expiration_date` varchar(10) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `credit_card`
--

INSERT INTO `credit_card` (`card_number`, `user_name`, `pin_code`, `expiration_date`, `user_id`) VALUES
('a', 'a', 2, 'a', 1),
('1234567812345678', 'Mihajlo Saric', 1234, '06/25', 2),
('1231231231231231', 'Marko Novic', 1234, '06/25', 4);

-- --------------------------------------------------------

--
-- Table structure for table `online_account`
--

CREATE TABLE `online_account` (
  `ID` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `online_account`
--

INSERT INTO `online_account` (`ID`, `user_id`) VALUES
(1, 1),
(2, 2),
(3, 4);

-- --------------------------------------------------------

--
-- Table structure for table `online_account_balance`
--

CREATE TABLE `online_account_balance` (
  `online_account_id` int(11) NOT NULL,
  `account_balance` varchar(50) NOT NULL,
  `currency` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `online_account_balance`
--

INSERT INTO `online_account_balance` (`online_account_id`, `account_balance`, `currency`) VALUES
(1, '1147.480751', 'USD'),
(1, '979.0', 'EUR'),
(3, '100.0', 'USD');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `ID` int(11) NOT NULL,
  `oa_from_ID` int(11) NOT NULL,
  `oa_to_ID` varchar(50) NOT NULL,
  `amount` varchar(50) NOT NULL,
  `currency` varchar(5) NOT NULL,
  `date_time` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`ID`, `oa_from_ID`, `oa_to_ID`, `amount`, `currency`, `date_time`) VALUES
(1, 1, '1', '1', 'USD', 'January 19, 2022 15:29:49'),
(2, 1, '1', '1', 'USD', 'January 19, 2022 15:32:03'),
(3, 1, '31', '10', 'EUR', 'January 19, 2022 15:32:56'),
(4, 1, '123123', '1', 'USD', 'January 19, 2022 15:37:53'),
(5, 1, '1', '1', 'USD', 'January 19, 2022 19:02:04');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `phone_number` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `first_name`, `last_name`, `address`, `city`, `country`, `phone_number`, `email`, `password`) VALUES
(1, 'Marko', 'Novic', 'Koce Kolarova 3', 'Novi Sad', 'Srbija', '0638196565', 'markonovic00@gmail.com', 'admin'),
(2, 'Mihajlo', 'Saric', 'Kapetana Berica 5', 'Novi Sad', 'Srbija', '0638196311', 'mihajlosaric7@gmail.com', 'kontrolarobe'),
(4, 'Marko', 'Novic', 'Koce Kolarova 3/5', 'Novi Sad', 'Serbia', '0637058537', 'markonovic@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `user_sessions`
--

CREATE TABLE `user_sessions` (
  `session_id` varchar(500) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_sessions`
--

INSERT INTO `user_sessions` (`session_id`, `user_id`) VALUES
('pbkdf2:sha256:150000$yhTkW9cT$6e26d3d0084393545c4868a4c7f1f5a3d99440721043569d735942df1c4125b0', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `credit_card`
--
ALTER TABLE `credit_card`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `online_account`
--
ALTER TABLE `online_account`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user_sessions`
--
ALTER TABLE `user_sessions`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `online_account`
--
ALTER TABLE `online_account`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
