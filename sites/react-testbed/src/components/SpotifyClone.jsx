import React, { useState } from "react";
import { Layout, Menu } from "antd";
import {
  Routes,
  Route,
  Link,
  useLocation,
  useSearchParams,
} from "react-router-dom";
import {
  HomeOutlined,
  SearchOutlined,
  UserOutlined,
  UnorderedListOutlined,
  AudioOutlined,
} from "@ant-design/icons";

import SpotifyHome from "./spotify/Home";
import Search from "./spotify/Search";
import ArtistProfile from "./spotify/ArtistProfile";
import MusicPlayer from "./spotify/MusicPlayer";
import artists from "./spotify/artistsData";
import Artists from "./spotify/Artists";
import Playlists from "./spotify/Playlists";
import playlistsData from "./spotify/playlistsData";
import SpotifyDataSharing from "./spotify/darkPatterns/SpotifyDataSharing";
import PricingPlans from './spotify/darkPatterns/AestheticManipulation';
import DecisionUncertainty from './spotify/darkPatterns/DecisionUncertainty';
import songs from "./spotify/songs";
import Podcasts from "./spotify/Podcasts";
import AestheticManipulation from "./spotify/darkPatterns/AestheticManipulation";
import "./SpotifyClone.css";
import Scratchpad from "./Scratchpad";

const randomMP3s = [
  "https://www.bensound.com/bensound-music/bensound-ukulele.mp3",
  "https://www.bensound.com/bensound-music/bensound-creativemind.mp3",
  "https://www.bensound.com/bensound-music/bensound-sunny.mp3",
  "https://www.bensound.com/bensound-music/bensound-energy.mp3",
  "https://www.bensound.com/bensound-music/bensound-dubstep.mp3"
];

const { Header, Content, Sider } = Layout;

const SpotifyClone = () => {
  const location = useLocation();
  const currentPath = location.pathname;

  const [currentSongIndex, setCurrentSongIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(50);
  const [playlists, setPlaylists] = useState(playlistsData);
  const [currentSequence, setCurrentSequence] = useState(songs);
  const [currentPodcastId, setCurrentPodcastId] = useState(null);

  const [searchParams] = useSearchParams();
  const darkPatternsParam = searchParams.get("dp");
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const playSong = (songId) => {
    const index = currentSequence.findIndex((song) => song.id === songId);
    if (index !== -1) {
      setCurrentSongIndex(index);
      setIsPlaying(true);
    }
  };

  const playPlaylist = (playlistSongs) => {
    setCurrentSequence(playlistSongs);
    setCurrentSongIndex(0);
    setIsPlaying(true);
  };

  const addSongToPlaylist = (playlistId, song) => {
    setPlaylists((prevPlaylists) =>
      prevPlaylists.map((playlist) =>
        playlist.id === playlistId
          ? { ...playlist, songs: [...playlist.songs, song] }
          : playlist
      )
    );
  };

  // New playPodcast function for podcasts
  const playPodcast = (podcast) => {
    const randomUrl = randomMP3s[Math.floor(Math.random() * randomMP3s.length)];
    const podcastTrack = { 
      title: podcast.title, 
      artist: podcast.host,
      audioSrc: randomUrl,
      coverArt: podcast.image 
    };
    setCurrentSequence([podcastTrack]);
    setCurrentSongIndex(0);
    setIsPlaying(true);
    setCurrentPodcastId(podcast.id);
  };

  return (
    <>
      <Layout className="spotify-layout" id="layoutMain">
        {selectedDarkPatterns.includes("du") && (
          <DecisionUncertainty id="decisionUncertainty" aria-label="Decision Uncertainty Modal" />          
        )}
        {selectedDarkPatterns.includes("ds") && (
          <SpotifyDataSharing id="spotifyDataSharing" aria-label="Spotify Data Sharing Information" />
        )}

        <Sider className="spotify-sider" id="siderMain" aria-label="Sidebar Navigation">
          <div className="spotify-logo" id="logoContainer">
            <Link to="/spotify" id="logoLink" aria-label="Spotify Home">
              <img
                src="https://cdn.freebiesupply.com/logos/large/2x/spotify-2-logo-png-transparent.png"
                alt="Spotify"
                id="logoImage"
                aria-label="Spotify Logo"
              />
            </Link>
          </div>
          <div className="sider-content" id="siderContent">
            <Menu
              theme="dark"
              mode="inline"
              selectedKeys={[currentPath]}
              className="spotify-menu"
              id="mainMenu"
              aria-label="Main Menu"
            >
              <Menu.Item key="/spotify" icon={<HomeOutlined />} id="menuHome" aria-label="Home">
                <Link to="/spotify" id="linkHome" aria-label="Navigate to Home">Home</Link>
              </Menu.Item>
              <Menu.Item key="/spotify/search" icon={<SearchOutlined />} id="menuSearch" aria-label="Search">
                <Link to="/spotify/search" id="linkSearch" aria-label="Navigate to Search">Search</Link>
              </Menu.Item>
              <Menu.Item key="/spotify/artists" icon={<UserOutlined />} id="menuArtists" aria-label="Artists">
                <Link to="/spotify/artists" id="linkArtists" aria-label="Navigate to Artists">Artists</Link>
              </Menu.Item>
              <Menu.Item
                key="/spotify/playlists"
                icon={<UnorderedListOutlined />}
                id="menuPlaylists"
                aria-label="Playlists"
              >
                <Link to="/spotify/playlists" id="linkPlaylists" aria-label="Navigate to Playlists">Playlists</Link>
              </Menu.Item>
              <Menu.Item key="/spotify/podcasts" icon={<AudioOutlined />} id="menuPodcasts" aria-label="Podcasts">
                <Link to="/spotify/podcasts" id="linkPodcasts" aria-label="Navigate to Podcasts">Podcasts</Link>
              </Menu.Item>
              <Menu.Item key="/spotify/membership" icon={<UserOutlined />} id="menuMembership" aria-label="Membership">
                <Link to="/spotify/membership" id="linkMembership" aria-label="Navigate to Membership">Membership</Link>
              </Menu.Item>
            </Menu>
          </div>
        </Sider>

        <Layout id="mainContentLayout">
          <Header className="spotify-header" id="headerMain" aria-label="Header"></Header>
          <Content className="spotify-content" id="contentArea" aria-label="Main Content">
            <Routes>
              <Route
                path="/"
                element={
                    <SpotifyHome
                      songs={currentSequence}
                      playSong={playSong}
                      playlists={playlists}
                      addSongToPlaylist={addSongToPlaylist}
                      id="spotifyHome"
                      aria-label="Spotify Home Page"
                    />
                }
              />
              <Route
                path="search"
                element={
                  <Search
                    songs={currentSequence}
                    artists={artists}
                    playSong={playSong}
                    playlists={playlists}
                    addSongToPlaylist={addSongToPlaylist}
                    id="searchPage"
                    aria-label="Search Page"
                  />
                }
              />
              <Route
                path="artists"
                element={
                  <Artists
                    artists={artists}
                    playSong={playSong}
                    id="artistsPage"
                    aria-label="Artists Page"
                  />
                }
              />
              <Route
                path="artist/:artistId"
                element={
                  <ArtistProfile
                    artists={artists}
                    songs={songs}
                    playSong={playSong}
                    playlists={playlists}
                    addSongToPlaylist={addSongToPlaylist}
                    id="artistProfile"
                    aria-label="Artist Profile Page"
                  />
                }
              />
              <Route
                path="playlists"
                element={
                  <Playlists
                    playlists={playlists}
                    songs={songs}
                    addSongToPlaylist={addSongToPlaylist}
                    playPlaylist={playPlaylist}
                    id="playlistsPage"
                    aria-label="Playlists Page"
                  />
                }
              />
              <Route
                path="podcasts"
                element={<Podcasts playPodcast={playPodcast} currentPodcastId={currentPodcastId} />}
              />
              <Route
                path="membership"
                element={<AestheticManipulation />}
              />
            </Routes>
          </Content>
          <MusicPlayer
            songs={currentSequence}
            currentSongIndex={currentSongIndex}
            isPlaying={isPlaying}
            setCurrentSongIndex={setCurrentSongIndex}
            setIsPlaying={setIsPlaying}
            volume={volume}
            setVolume={setVolume}
            id="musicPlayer"
            aria-label="Music Player"
          />
        </Layout>
      </Layout>
      <Scratchpad />
    </>
  );
};

export default SpotifyClone;
