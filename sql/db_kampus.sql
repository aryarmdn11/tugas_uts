-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 03, 2026 at 05:33 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_kampus`
--

-- --------------------------------------------------------

--
-- Table structure for table `dosen`
--

CREATE TABLE `dosen` (
  `nidn` varchar(20) NOT NULL,
  `nm_dosen` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_prodi` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dosen`
--

INSERT INTO `dosen` (`nidn`, `nm_dosen`, `email`, `id_prodi`) VALUES
('D001', 'Sumenep', 'sumenep@gmail.com', 1),
('D002', 'Supriyadi', 'supri@gmail.com', 2),
('D003', 'Mulyadi', 'mul@gmail.com', 3),
('D004', 'Arman', 'arman@gmail.com', 4),
('D005', 'Sumanto', 'sumanto@gmail.com', 5),
('D006', 'Asep', 'asep@gmail.com', 6),
('D007', 'Udin', 'udin@gmail.com', 7),
('D008', 'Citra Lestari', 'citra@gmail.com', 8),
('D009', 'Gina Maharani', 'gina@gmail.com', 9),
('D010', 'Intan Permata', 'intan@gmail.com', 10);

-- --------------------------------------------------------

--
-- Table structure for table `krs`
--

CREATE TABLE `krs` (
  `id_krs` int(11) NOT NULL,
  `nim` varchar(20) DEFAULT NULL,
  `id_mk` int(11) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL,
  `th_akademik` varchar(10) DEFAULT NULL,
  `nilai` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `krs`
--

INSERT INTO `krs` (`id_krs`, `nim`, `id_mk`, `semester`, `th_akademik`, `nilai`) VALUES
(1, '25001', 1, 3, '2025/2026', '4.0'),
(2, '25002', 2, 3, '2025/2026', '3.76'),
(3, '25003', 3, 3, '2025/2026', '3.95'),
(4, '25004', 4, 3, '2025/2026', '3.70'),
(5, '25005', 5, 3, '2025/2026', '3.80'),
(6, '25006', 6, 3, '2025/2026', '4.0'),
(7, '25007', 7, 3, '2025/2026', '4.0'),
(8, '25008', 8, 3, '2025/2026', '4.0'),
(9, '25009', 9, 3, '2025/2026', '3.99'),
(10, '25010', 10, 3, '2025/2026', '3.89');

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `nim` varchar(20) NOT NULL,
  `nm_mahasiswa` varchar(100) DEFAULT NULL,
  `jns_kelamin` varchar(10) DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `id_prodi` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`nim`, `nm_mahasiswa`, `jns_kelamin`, `tgl_lahir`, `alamat`, `id_prodi`) VALUES
('25001', 'Aditya Saputra', 'L', '2006-01-12', 'Tangerang', 1),
('25002', 'Bella Saputri', 'P', '2006-03-20', 'Jakarta', 2),
('25003', 'Candra Wijaya', 'L', '2006-07-15', 'Depok', 3),
('25004', 'Dinda Amelia', 'P', '2006-05-09', 'Bogor', 4),
('25005', 'Eko Prasetyo', 'L', '2005-11-23', 'Bekasi', 5),
('25006', 'Fitri Handayani', 'P', '2006-02-14', 'Serang', 6),
('25007', 'Gilang', 'L', '2006-09-30', 'Cilegon', 7),
('25008', 'Hana Safitri', 'P', '2005-10-11', 'Garut', 8),
('25009', 'Ilham Maulana', 'L', '2006-10-11', 'Tasikmalaya', 9),
('25010', 'Jasmine Aulia', 'P', '2006-11-10', 'Cimahi', 10);

-- --------------------------------------------------------

--
-- Table structure for table `mata_kuliah`
--

CREATE TABLE `mata_kuliah` (
  `id_mk` int(11) NOT NULL,
  `nm_mk` varchar(100) DEFAULT NULL,
  `sks` int(11) DEFAULT NULL,
  `nidn` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mata_kuliah`
--

INSERT INTO `mata_kuliah` (`id_mk`, `nm_mk`, `sks`, `nidn`) VALUES
(1, 'Algoritma dan Pemrograman', 3, 'D001'),
(2, 'Rangkaian Listrik', 3, 'D002'),
(3, 'Manajemen Operasional', 3, 'D003'),
(4, 'Konversi Energi', 3, 'D004'),
(5, 'Pemrograman Web', 3, 'D005'),
(6, 'Desain Grafis', 3, 'D006'),
(7, 'Teori Komunikasi', 3, 'D007'),
(8, 'Pengantar Akuntansi', 2, 'D008'),
(9, 'Manajemen Umum', 2, 'D009'),
(10, 'Matematika Syariah', 2, 'D010');

-- --------------------------------------------------------

--
-- Table structure for table `prodi`
--

CREATE TABLE `prodi` (
  `id_prodi` int(11) NOT NULL,
  `nm_prodi` varchar(100) DEFAULT NULL,
  `jenjang` varchar(10) DEFAULT NULL,
  `akreditasi` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prodi`
--

INSERT INTO `prodi` (`id_prodi`, `nm_prodi`, `jenjang`, `akreditasi`) VALUES
(1, 'Teknik Informatika', 'S1', 'A'),
(2, 'Teknik Elektro', 'S1', 'A'),
(3, 'Teknik Industri', 'S1', 'A'),
(4, 'Teknik Mesin', 'S1', 'A'),
(5, 'Sistem Informasi', 'S1', 'A'),
(6, 'Desain Komunikasi Visual', 'S1', 'A'),
(7, 'Ilmu Komunikasi', 'D4', 'B'),
(8, 'Akuntansi', 'S1', 'A'),
(9, 'Manajemen', 'D4', 'B'),
(10, 'Ekonomi Syariah', 'S1', 'A');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`nidn`),
  ADD KEY `id_prodi` (`id_prodi`);

--
-- Indexes for table `krs`
--
ALTER TABLE `krs`
  ADD PRIMARY KEY (`id_krs`),
  ADD KEY `nim` (`nim`),
  ADD KEY `id_mk` (`id_mk`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`nim`),
  ADD KEY `id_prodi` (`id_prodi`);

--
-- Indexes for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  ADD PRIMARY KEY (`id_mk`),
  ADD KEY `nidn` (`nidn`);

--
-- Indexes for table `prodi`
--
ALTER TABLE `prodi`
  ADD PRIMARY KEY (`id_prodi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `krs`
--
ALTER TABLE `krs`
  MODIFY `id_krs` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  MODIFY `id_mk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `prodi`
--
ALTER TABLE `prodi`
  MODIFY `id_prodi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dosen`
--
ALTER TABLE `dosen`
  ADD CONSTRAINT `dosen_ibfk_1` FOREIGN KEY (`id_prodi`) REFERENCES `prodi` (`id_prodi`);

--
-- Constraints for table `krs`
--
ALTER TABLE `krs`
  ADD CONSTRAINT `krs_ibfk_1` FOREIGN KEY (`nim`) REFERENCES `mahasiswa` (`nim`),
  ADD CONSTRAINT `krs_ibfk_2` FOREIGN KEY (`id_mk`) REFERENCES `mata_kuliah` (`id_mk`);

--
-- Constraints for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD CONSTRAINT `mahasiswa_ibfk_1` FOREIGN KEY (`id_prodi`) REFERENCES `prodi` (`id_prodi`);

--
-- Constraints for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  ADD CONSTRAINT `mata_kuliah_ibfk_1` FOREIGN KEY (`nidn`) REFERENCES `dosen` (`nidn`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
