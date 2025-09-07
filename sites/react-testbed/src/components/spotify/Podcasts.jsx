import React, { useState } from "react";
import podcasts from "./podcastsData";
import "./Podcasts.css";

const randomMP3s = [
  "https://www.bensound.com/bensound-music/bensound-ukulele.mp3",
  "https://www.bensound.com/bensound-music/bensound-creativeminds.mp3",
  "https://www.bensound.com/bensound-music/bensound-sunny.mp3",
  "https://www.bensound.com/bensound-music/bensound-energy.mp3",
  "https://www.bensound.com/bensound-music/bensound-dubstep.mp3"
];

const Podcasts = (props) => {
  const [followedPodcasts, setFollowedPodcasts] = useState({});

  const toggleFollowPodcast = (podcastId) => {
    setFollowedPodcasts(prev => ({ ...prev, [podcastId]: !prev[podcastId] }));
  };

  return (
    <div className="podcasts-section" id="podcastsSection">
      <h2>Podcasts</h2>
      <div className="podcasts-grid">
        {podcasts.map((podcast) => (
          <div key={podcast.id} className="podcast-card">
            {/* Podcast image */}
            <img
              src={podcast.image}
              alt={`${podcast.title} Cover`}
              className="podcast-cover"
              style={{ width: "150px", height: "150px", objectFit: "cover" }}
            />
            <h3>{podcast.title}</h3>
            <p>
              <strong>Host:</strong> {podcast.host}
            </p>
            <p>{podcast.description}</p>
            <p>
              <strong>Rating:</strong> {podcast.rating} / 5
            </p>
            {/* Display categories */}
            <p>
              <strong>Categories:</strong> {podcast.categories.join(", ")}
            </p>
            <button
              onClick={() => props.playPodcast(podcast)}
              id={`play-podcast-${podcast.id}`}
              aria-label={`Play ${podcast.title} podcast`}
            >
              {props.currentPodcastId === podcast.id ? (
                <>
                  <span className="playing-indicator"></span> Playing Podcast
                </>
              ) : (
                "Play Podcast"
              )}
            </button>
            {/* New Follow/Unfollow button */}
            <button
              onClick={() => toggleFollowPodcast(podcast.id)}
              id={`follow-podcast-${podcast.id}`}
              aria-label={`${followedPodcasts[podcast.id] ? "Unfollow" : "Follow"} ${podcast.title}`}
              style={{ marginTop: "10px" }}
            >
              {followedPodcasts[podcast.id] ? "Unfollow" : "Follow"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Podcasts;
