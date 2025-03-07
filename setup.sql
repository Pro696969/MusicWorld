-- Active: 1726423656028@@127.0.0.1@3306@DBT25_A1_PES2UG22CS281_Krishna
CREATE DATABASE DBT25_A1_PES2UG22CS281_Krishna;
USE DBT25_A1_PES2UG22CS281_Krishna;

CREATE TABLE Artists (
    ArtistID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(100),
    BirthYear INT,
    Biography TEXT
);

CREATE TABLE Albums (
    AlbumID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    MainArtistID INT,
    ReleaseDate DATE,
    Label VARCHAR(255),
    TotalTracks INT,
    AlbumType VARCHAR(100),
    CoverArtURL VARCHAR(500),
    FOREIGN KEY (MainArtistID) REFERENCES Artists(ArtistID)
);

CREATE TABLE Tracks (
    TrackID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Duration TIME,
    BPM INT,
    MoodTags VARCHAR(255),
    Explicit BOOLEAN,
    LyricsURL VARCHAR(500),
    AlbumID INT,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
);

CREATE TABLE Collaborations (
    CollaborationID INT AUTO_INCREMENT PRIMARY KEY,
    TrackID INT,
    ArtistID INT,
    Role VARCHAR(100),
    FOREIGN KEY (TrackID) REFERENCES Tracks(TrackID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
);

CREATE TABLE Playlists (
    PlaylistID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    TrackID INT,
    Creator VARCHAR(255),
    CreationDate DATE,
    Description TEXT,
    IsPublic BOOLEAN,
    PlaylistTracks TEXT,
    FOREIGN KEY (TrackID) REFERENCES Tracks(TrackID)
);
CREATE TABLE Genres (
    GenreID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    ParentGenre INT,
    FOREIGN KEY (ParentGenre) REFERENCES Genres(GenreID)
);

CREATE TABLE ArtistGenres (
    ArtistID INT,
    GenreID INT,
    PRIMARY KEY (ArtistID, GenreID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
);

SHOW TABLES; 

INSERT INTO `Artists` (ArtistID, Name, Country, BirthYear, Biography)
VALUES (10001, "KK", "India", "2004", "hi i am kk");

UPDATE `Artists`
SET `Biography` = "PES2UG22CS281"
WHERE `ArtistID` = 10001;

SELECT * FROM `Artists`
WHERE `ArtistID` = 10001;