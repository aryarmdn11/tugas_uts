
CREATE DATABASE IF NOT EXISTS db_kampus
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE db_kampus;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS krs;
DROP TABLE IF EXISTS mata_kuliah;
DROP TABLE IF EXISTS mahasiswa;
DROP TABLE IF EXISTS dosen;
DROP TABLE IF EXISTS prodi;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE prodi (
  id_prodi   INT AUTO_INCREMENT PRIMARY KEY,
  nm_prodi   VARCHAR(100) NOT NULL,
  jenjang    VARCHAR(10)  NOT NULL,
  akreditasi CHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dosen (
  nidn     VARCHAR(20) PRIMARY KEY,
  nm_dosen VARCHAR(100) NOT NULL,
  email    VARCHAR(100),
  id_prodi INT,
  CONSTRAINT fk_dosen_prodi FOREIGN KEY (id_prodi)
    REFERENCES prodi (id_prodi) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE mahasiswa (
  nim          VARCHAR(20) PRIMARY KEY,
  nm_mahasiswa VARCHAR(100) NOT NULL,
  jns_kelamin  VARCHAR(10),
  tgl_lahir    DATE,
  alamat       TEXT,
  id_prodi     INT,
  CONSTRAINT fk_mhs_prodi FOREIGN KEY (id_prodi)
    REFERENCES prodi (id_prodi) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE mata_kuliah (
  id_mk INT AUTO_INCREMENT PRIMARY KEY,
  nm_mk VARCHAR(100) NOT NULL,
  sks   INT NOT NULL,
  nidn  VARCHAR(20),
  CONSTRAINT fk_mk_dosen FOREIGN KEY (nidn)
    REFERENCES dosen (nidn) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE krs (
  id_krs      INT AUTO_INCREMENT PRIMARY KEY,
  nim         VARCHAR(20) NOT NULL,
  id_mk       INT NOT NULL,
  semester    INT NOT NULL,
  th_akademik VARCHAR(10) NOT NULL,
  nilai       VARCHAR(10),
  CONSTRAINT fk_krs_mhs FOREIGN KEY (nim)
    REFERENCES mahasiswa (nim) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_krs_mk FOREIGN KEY (id_mk)
    REFERENCES mata_kuliah (id_mk) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO prodi (nm_prodi, jenjang, akreditasi) VALUES
  ('Teknik Informatika', 'S1', 'A'),
  ('Sistem Informasi',   'S1', 'B'),
  ('Manajemen',          'S1', 'A'),
  ('Akuntansi',          'D3', 'B');

INSERT INTO dosen (nidn, nm_dosen, email, id_prodi) VALUES
  ('0401018801', 'Dr. Budi Santoso, M.Kom', 'budi.santoso@kampus.ac.id', 1),
  ('0402029002', 'Siti Aminah, M.T.',       'siti.aminah@kampus.ac.id',  1),
  ('0403038503', 'Rudi Hartono, M.Si.',     'rudi.hartono@kampus.ac.id', 2),
  ('0404048704', 'Dewi Lestari, M.M.',      'dewi.lestari@kampus.ac.id', 3);

INSERT INTO mahasiswa (nim, nm_mahasiswa, jns_kelamin, tgl_lahir, alamat, id_prodi) VALUES
  ('2024010001', 'Andi Pratama',   'Laki-laki', '2005-03-14', 'Jl. Merdeka No. 10, Jakarta',    1),
  ('2024010002', 'Rina Kusuma',    'Perempuan', '2005-07-22', 'Jl. Sudirman No. 5, Bandung',    1),
  ('2024020001', 'Bagas Wijaya',   'Laki-laki', '2004-11-02', 'Jl. Diponegoro No. 21, Bekasi',  2),
  ('2024020002', 'Citra Maharani', 'Perempuan', '2005-01-30', 'Jl. Ahmad Yani No. 8, Depok',    2),
  ('2024030001', 'Dimas Saputra',  'Laki-laki', '2004-09-18', 'Jl. Gatot Subroto No. 3, Bogor', 3),
  ('2024040001', 'Eka Fitriani',   'Perempuan', '2005-05-09', 'Jl. Pahlawan No. 15, Tangerang', 4);

INSERT INTO mata_kuliah (nm_mk, sks, nidn) VALUES
  ('Basis Data',            3, '0401018801'),
  ('Pemrograman Web',       3, '0402029002'),
  ('Analisis Sistem',       2, '0403038503'),
  ('Pengantar Manajemen',   2, '0404048704'),
  ('Algoritma dan Pemrograman', 4, '0402029002');

INSERT INTO krs (nim, id_mk, semester, th_akademik, nilai) VALUES
  ('2024010001', 1, 3, '2025/2026', 'A'),
  ('2024010001', 2, 3, '2025/2026', 'B+'),
  ('2024010002', 1, 3, '2025/2026', 'A-'),
  ('2024010002', 5, 3, '2025/2026', 'B'),
  ('2024020001', 3, 3, '2025/2026', 'B'),
  ('2024020002', 3, 3, '2025/2026', 'A'),
  ('2024030001', 4, 3, '2025/2026', 'B+'),
  ('2024040001', 4, 1, '2025/2026', NULL);
