SELECT COUNT(*) FROM `Artists`;
SELECT COUNT(*) FROM `Albums`;
SELECT COUNT(*) FROM `Collaborations`;
SELECT COUNT(*) FROM `Genres`;
SELECT COUNT(*) FROM `Playlists`;
SELECT COUNT(*) FROM `Tracks`;
SELECT TrackID FROM `Tracks`;
SELECT COUNT(*) FROM `Playlists`;

-- Query to find all song details where specific Artist collaborated
EXPLAIN ANALYZE SELECT t.TrackID, t.title, a.Name AS MainArtist, c.Role
FROM `Tracks` t
JOIN `Albums` al ON t.`AlbumID` = al.`AlbumID`
JOIN `Artists` a ON al.`MainArtistID` = a.`ArtistID`
JOIN `Collaborations` c ON t.`TrackID` = c.`TrackID`
JOIN `Artists` collaber ON c.`ArtistID` = collaber.`ArtistID`
WHERE collaber.`Name` = "Laura Williams";

-- Find the Top 10 Most Collaborative Artists
SELECT a.ArtistID, a.Name, COUNT(c.CollaborationID) AS NumCollaborations
FROM Artists a
JOIN Collaborations c ON a.ArtistID = c.ArtistID
GROUP BY a.ArtistID, a.Name
ORDER BY NumCollaborations DESC
LIMIT 10;

-- Find Albums with the Most Collaborations
EXPLAIN ANALYZE SELECT al.AlbumID, al.Title, al.MainArtistID, COUNT(c.CollaborationID) AS MaxCOllabs
FROM `Albums` al
JOIN `Tracks` t ON t.`AlbumID` = al.`AlbumID`
JOIN `Collaborations` c ON c.`TrackID` = t.`TrackID`
GROUP BY al.`AlbumID`, al.`Title`
ORDER BY MaxCollabs DESC 
LIMIT 10;

SHOW INDEXES FROM `Artists`;

EXPLAIN ANALYZE SELECT * FROM `Artists` WHERE `Biography` = "PES2UG22CS281";

EXPLAIN ANALYZE SELECT * FROM `Artists` WHERE `ArtistID` = 587;
DROP INDEX pri_artistID ON Artists;

CREATE INDEX main_artist_Albums ON Albums(MainArtistID);
CREATE INDEX artistID_Collab ON Collaborations(ArtistID);
CREATE INDEX trackID_Collab ON Collaborations(TrackID);
CREATE INDEX albumID_Tracks ON Tracks(AlbumID);

SHOW INDEXES FROM `Collaborations`;

SELECT t.TrackID, t.Title, a.Name AS MainArtist, c.Role
FROM Artists collaber

-- Start with the Most Selective Join for i)
EXPLAIN ANALYZE 
SELECT t.TrackID, t.Title, a.Name AS MainArtist, c.Role
FROM `Artists` collaber 
JOIN `Collaborations` c ON collaber.ArtistID = c.ArtistID
JOIN `Tracks` t ON c.TrackID = t.TrackID
JOIN `Albums` al ON t.AlbumID = al.AlbumID
JOIN `Artists` a ON al.MainArtistID = a.ArtistID
WHERE collaber.`Name` = "Laura Williams";

-- Using a Subquery to Pre-Filter Data for i)
EXPLAIN ANALYZE
SELECT t.TrackID, t.Title, a.Name AS MainArtist, c.Role
FROM (
    SELECT c.TrackID
    FROM `Collaborations` c
    JOIN `Artists` collaber ON collaber.`ArtistID` = c.`ArtistID`
    WHERE collaber.`Name` = "Laura Williams"
) preFilter 
JOIN `Tracks` t ON preFilter.`TrackID` = t.`TrackID`
JOIN `Albums` al ON t.`AlbumID` = al.`AlbumID`
JOIN `Artists` a ON al.`MainArtistID` = a.`ArtistID`
JOIN `Collaborations` c on t.`TrackID` = c.`TrackID`;

-- Outer Join
EXPLAIN ANALYZE 
SELECT t.TrackID, t.Title, a.Name AS MainArtist, c.Role
FROM `Tracks` t
LEFT JOIN `Collaborations` c ON t.`TrackID` = c.`TrackID`
LEFT JOIN Artists collaber ON c.`ArtistID` = collaber.`ArtistID` AND collaber.`Name` = "Laura Williams"
JOIN Albums al ON t.AlbumID = al.AlbumID
JOIN Artists a ON al.`MainArtistID` = a.`ArtistID`;

