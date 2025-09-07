import React, { useState } from "react";
import "./Artists.css"; // new artists styling

const Artists = ({ artists, playSong }) => {
  const [followedArtists, setFollowedArtists] = useState({});

  const toggleFollow = (artistId) => {
    setFollowedArtists(prev => ({ ...prev, [artistId]: !prev[artistId] }));
  };

  return (
    <div className="artists-list">
      <div className="artists-grid">
        {artists.map((artist) => (
          <div key={artist.id} className="artist-card" id={`artist-card-${artist.id}`} aria-label={`Artist ${artist.name} Card`}>
            <img
              src={artist.avatar}
              alt={`${artist.name} Avatar`}
              className="artist-avatar"
              id={`artist-avatar-${artist.id}`}
            />
            <h3 id={`artist-name-${artist.id}`}>{artist.name}</h3>
            <p id={`artist-bio-${artist.id}`}>{artist.bio}</p>
            <button
              onClick={() => toggleFollow(artist.id)}
              aria-label={`Follow ${artist.name}`}
              id={`follow-button-${artist.id}`}
            >
              {followedArtists[artist.id] ? "Unfollow" : "Follow"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Artists;
