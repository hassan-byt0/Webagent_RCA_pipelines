import React, { useRef, useEffect, useState } from "react";
import { Layout, Slider, Button, Row, Col } from "antd";
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  StepBackwardOutlined,
  StepForwardOutlined,
  SoundOutlined,
  SoundFilled,
} from "@ant-design/icons";

const { Footer } = Layout;

const MusicPlayer = ({
  songs, // Now represents the current sequence
  currentSongIndex,
  isPlaying,
  setCurrentSongIndex,
  setIsPlaying,
  volume,
  setVolume,
}) => {
  const audioRef = useRef(new Audio(songs[currentSongIndex].audioSrc));
  const [isMuted, setIsMuted] = useState(false);

  useEffect(() => {
    const audio = audioRef.current;
    audio.src = songs[currentSongIndex].audioSrc;
    audio.volume = volume / 100;
    audio.muted = isMuted;
    if (isPlaying) {
      audio.play();
    }
    return () => {
      audio.pause();
    };
  }, [currentSongIndex, isPlaying, songs, volume, isMuted]);

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
    if (!isPlaying) {
      audioRef.current.play();
    } else {
      audioRef.current.pause();
    }
  };

  const handlePrev = () => {
    const prevIndex = (currentSongIndex - 1 + songs.length) % songs.length;
    setCurrentSongIndex(prevIndex);
    setIsPlaying(true);
  };

  const handleNext = () => {
    const nextIndex = (currentSongIndex + 1) % songs.length;
    setCurrentSongIndex(nextIndex);
    setIsPlaying(true);
  };

  const handleVolumeChange = (value) => {
    setVolume(value);
    audioRef.current.volume = value / 100;
    if (value > 0 && isMuted) {
      setIsMuted(false);
      audioRef.current.muted = false;
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
    audioRef.current.muted = !isMuted;
  };

  const currentSong = songs[currentSongIndex];

  return (
    <Footer
      className="spotify-music-player"
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "20px",
        background: "#001529",
      }}
    >
      <Row
        justify="center"
        align="middle"
        style={{ width: "100%", maxWidth: "800px" }}
      >
        <Col>
          <div
            className="player-info"
            style={{ textAlign: "center", color: "#fff" }}
          >
            <strong>{currentSong.title}</strong> - {currentSong.artist}
          </div>
        </Col>
        <Col>
          <div
            className="player-controls"
            style={{ display: "flex", gap: "10px", margin: "0 20px" }}
          >
            <Button
              icon={<StepBackwardOutlined />}
              id="previous-button"
              aria-label="Previous Song"
              onClick={handlePrev}
            />
            <Button
              icon={
                isPlaying ? <PauseCircleOutlined /> : <PlayCircleOutlined />
              }
              id="play-pause-button"
              aria-label={isPlaying ? "Pause Song" : "Play Song"}
              onClick={handlePlayPause}
              size="large"
            />
            <Button
              icon={<StepForwardOutlined />}
              id="next-button"
              aria-label="Next Song"
              onClick={handleNext}
            />
          </div>
        </Col>
        <Col>
          <div style={{ display: "flex", alignItems: "center" }}>
            <Slider
              id="volume-slider"
              aria-label="Volume Control"
              min={0}
              max={100}
              value={volume}
              onChange={handleVolumeChange}
              style={{ width: 100, marginRight: 10 }}
            />
            <Button
              type="text"
              id="mute-button"
              aria-label={isMuted ? "Unmute" : "Mute"}
              onClick={toggleMute}
              icon={
                isMuted ? (
                  <SoundOutlined style={{ color: "#fff" }} />
                ) : (
                  <SoundFilled style={{ color: "#fff" }} />
                )
              }
            />
          </div>
        </Col>
      </Row>
    </Footer>
  );
};

export default MusicPlayer;
