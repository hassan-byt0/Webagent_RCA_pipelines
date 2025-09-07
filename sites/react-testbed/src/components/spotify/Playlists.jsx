import React from "react";
import { List, Card, Button, Modal, Select } from "antd";
import { PlayCircleOutlined } from "@ant-design/icons";

const { Option } = Select;

const Playlists = ({ playlists, songs, addSongToPlaylist, playPlaylist }) => {
  const [isModalVisible, setIsModalVisible] = React.useState(false);
  const [selectedPlaylist, setSelectedPlaylist] = React.useState(null);
  const [songToAdd, setSongToAdd] = React.useState(null);
  const [selectedSongId, setSelectedSongId] = React.useState(null);
  const [currentPlaylistId, setCurrentPlaylistId] = React.useState(null);

  const showModal = (playlistId) => {
    setIsModalVisible(true);
    setCurrentPlaylistId(playlistId);
  };

  const handleOk = () => {
    if (currentPlaylistId && selectedSongId) {
      const songToAdd = songs.find((song) => song.id === selectedSongId);
      if (songToAdd) {
        addSongToPlaylist(currentPlaylistId, songToAdd);
      }
    }
    setIsModalVisible(false);
    setSelectedSongId(null);
    setCurrentPlaylistId(null);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedPlaylist(null);
    setSongToAdd(null);
  };

  const handlePlayPlaylist = (playlist) => {
    playPlaylist(playlist.songs);
  };

  return (
    <div className="spotify-playlists">
      <h2>Your Playlists</h2>
      <List
        grid={{ gutter: 16, column: 2 }}
        dataSource={playlists}
        renderItem={(playlist) => (
          <List.Item>
            <Card
              title={playlist.name}
              actions={[
                <PlayCircleOutlined
                  key="play"
                  id={`play-playlist-${playlist.id}`}
                  aria-label={`Play ${playlist.name} playlist`}
                  onClick={() => handlePlayPlaylist(playlist)}
                />,
                <Button
                  type="link"
                  id={`add-song-${playlist.id}`}
                  aria-label={`Add song to ${playlist.name} playlist`}
                  onClick={() => showModal(playlist.id)}
                >
                  Add Song
                </Button>,
              ]}
            >
              <List
                dataSource={playlist.songs}
                renderItem={(song) => (
                  <List.Item>
                    {song.title} - {song.artist}
                  </List.Item>
                )}
              />
            </Card>
          </List.Item>
        )}
      />
      <Modal
        title="Add Song to Playlist"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        aria-label="Add Song to Playlist Modal"
      >
        <Select
          id="song-select"
          aria-label="Select a song to add"
          style={{ width: "100%" }}
          placeholder="Select a song"
          onChange={(value) => setSelectedSongId(value)}
        >
          {songs.map((song) => (
            <Option key={song.id} value={song.id}>
              {song.title} - {song.artist}
            </Option>
          ))}
        </Select>
      </Modal>
    </div>
  );
};
export default Playlists;
