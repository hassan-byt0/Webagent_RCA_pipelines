import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { Typography, List, Card, Button, Modal, Select } from "antd";
import { PlayCircleOutlined } from "@ant-design/icons";

const { Title, Paragraph } = Typography;
const { Option } = Select;

const ArtistProfile = ({
  artists,
  songs,
  playSong,
  playlists,
  addSongToPlaylist,
}) => {
  const { artistId } = useParams();
  const artist = artists.find((a) => a.id === artistId);
  const artistSongs = songs.filter((song) => song.artistId === artistId);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [songToAdd, setSongToAdd] = useState(null);
  const [isFollowed, setIsFollowed] = useState(false);

  const toggleFollow = () => setIsFollowed((prev) => !prev);

  const showAddModal = (song) => {
    setIsModalVisible(true);
    setSongToAdd(song);
  };

  const handleAddOk = () => {
    if (selectedPlaylist && songToAdd) {
      addSongToPlaylist(selectedPlaylist, songToAdd);
    }
    setIsModalVisible(false);
    setSelectedPlaylist(null);
    setSongToAdd(null);
  };

  const handleAddCancel = () => {
    setIsModalVisible(false);
    setSelectedPlaylist(null);
    setSongToAdd(null);
  };

  if (!artist) {
    return <div>Artist not found.</div>;
  }

  return (
    <div className="spotify-artist-profile">
      <Title level={2} id="artist-name">{artist.name}</Title>
      <img src={artist.avatar} alt={artist.name} className="artist-avatar" id="artist-avatar" />
      <Paragraph id="artist-bio">{artist.bio}</Paragraph>
      <button
        onClick={toggleFollow}
        aria-label={`Follow ${artist.name}`}
        id={`artist-profile-follow-button-${artist.id}`}
      >
        {isFollowed ? "Unfollow" : "Follow"}
      </button>
      <Title level={3}>Songs</Title>
      <List
        grid={{ gutter: 16, xs: 1, sm: 2, md: 4, lg: 4 }}
        dataSource={artistSongs}
        renderItem={(song) => (
          <List.Item>
            <Card
              hoverable
              cover={<img alt={song.title} src={song.coverArt} id={`artist-song-cover-${song.id}`} />}
              actions={[
                <PlayCircleOutlined
                  key="play"
                  id={`artist-play-button-${song.id}`}
                  aria-label={`Play ${song.title}`}
                  onClick={() => playSong(song.id)}
                />,
                <Button
                  type="link"
                  id={`artist-add-to-playlist-${song.id}`}
                  aria-label={`Add ${song.title} to playlist`}
                  onClick={() => showAddModal(song)}
                >
                  Add to Playlist
                </Button>,
              ]}
            >
              <Card.Meta title={song.title} description={song.album} />
            </Card>
          </List.Item>
        )}
      />
      <Modal
        title="Add Song to Playlist"
        visible={isModalVisible}
        onOk={handleAddOk}
        onCancel={handleAddCancel}
        aria-label="Add Song to Playlist Modal"
      >
        <Select
          id="artist-playlist-select"
          aria-label="Select a playlist to add the song"
          style={{ width: "100%" }}
          placeholder="Select a playlist"
          onChange={(value) => setSelectedPlaylist(value)}
        >
          {playlists.map((playlist) => (
            <Option key={playlist.id} value={playlist.id}>
              {playlist.name}
            </Option>
          ))}
        </Select>
      </Modal>
    </div>
  );
};

export default ArtistProfile;
