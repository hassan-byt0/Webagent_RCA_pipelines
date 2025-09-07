import React, { useState } from "react";
import { Input, List, Card, Button, Modal, Select } from "antd";
import { Link } from "react-router-dom";
import { PlayCircleOutlined } from "@ant-design/icons";

const { Search: AntSearch } = Input;
const { Option } = Select;

const Search = ({ songs, artists, playSong, playlists, addSongToPlaylist }) => {
  const [query, setQuery] = useState("");
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [songToAdd, setSongToAdd] = useState(null);

  const filteredSongs = songs.filter(
    (song) =>
      song.title.toLowerCase().includes(query.toLowerCase()) ||
      artists
        .find((artist) => artist.id === song.artistId)
        ?.name.toLowerCase()
        .includes(query.toLowerCase())
  );

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

  return (
    <div className="spotify-search">
      <AntSearch
        id="search-input"
        aria-label="Search for songs or artists"
        placeholder="Search for songs or artists"
        enterButton
        size="large"
        onSearch={(value) => setQuery(value)}
        style={{ marginBottom: "20px", maxWidth: "600px" }}
      />
      <List
        grid={{ gutter: 16, column: 4 }}
        dataSource={filteredSongs}
        renderItem={(song) => (
          <List.Item>
            <Card
              hoverable
              cover={<img alt={song.title} src={song.coverArt} />}
              actions={[
                <PlayCircleOutlined
                  key="play"
                  id={`play-button-${song.id}`}
                  aria-label={`Play ${song.title}`}
                  onClick={() => playSong(song.id)}
                />,
                <Button
                  type="link"
                  id={`add-to-playlist-${song.id}`}
                  aria-label={`Add ${song.title} to playlist`}
                  onClick={() => showAddModal(song)}
                >
                  Add to Playlist
                </Button>,
              ]}
            >
              <Card.Meta
                title={song.title}
                description={
                  <Link to={`/spotify/artist/${song.artistId}`}>
                    {
                      artists.find((artist) => artist.id === song.artistId)
                        ?.name
                    }
                  </Link>
                }
              />
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
        okButtonProps={{ id: "add-song-ok-button" }}
        cancelButtonProps={{ id: "add-song-cancel-button" }}
      >
        <Select
          id="playlist-select"
          aria-label="Select a playlist"
          style={{ width: "100%" }}
          placeholder="Select a playlist"
          onChange={(value) => setSelectedPlaylist(value)}
        >
          {playlists.map((playlist) => (
            <Option id={`add-to-playlist-${playlist.name}`} key={playlist.id} value={playlist.id}>
              {playlist.name}
            </Option>
          ))}
        </Select>
      </Modal>
    </div>
  );
};

export default Search;
