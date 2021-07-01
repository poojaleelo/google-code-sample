"""A video player class."""

from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.videos_list = self._video_library.get_all_videos()
        self.playlists = []
        self.playlists_tracks = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos: ")

        videos_data = []
        for video in self.videos_list:
            videos_data.append(video.title + " (" + str(video.video_id) + ") ""[" + self.extract_tags(video.tags) + "]")
        # print("show_all_videos needs implementation")

        videos_data.sort()
        for data in videos_data:
            print(data)

    def extract_tags(self, tags):
        extracted = ""
        for i in range(len(tags)):
            extracted += tags[i]
            if i < (len(tags) - 1):
                extracted += " "

        return extracted

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        found = False
        for video in self.videos_list:
            if video.video_id == video_id:
                found = True
                for videostop in self.videos_list:
                    if videostop.playing:
                        print("Stopping video: " + videostop.title)
                        if videostop.pause:
                            videostop.change_pause()
                        videostop.change_state()
                video.change_state()
                print("Playing video: " + video.title)
        if not found:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        found = False
        for video in self.videos_list:
            if video.playing:
                found = True
                print("Stopping video: " + video.title)
                video.change_state()
        if not found:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        for video in self.videos_list:
            if video.playing:
                print("Stopping video: " + video.title)
                video.change_state()
        video_random = random.choice(self.videos_list)
        video_random.change_state()
        print("Playing video: " + video_random.title)

    def pause_video(self):
        """Pauses the current video."""
        found = False
        for video in self.videos_list:
            if video.pause:
                print("Video already paused: " + video.title)
                found = True
            elif video.playing:
                found = True
                print("Pausing video: " + video.title)
                video.change_pause()

        if not found:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        found = False

        for video in self.videos_list:
            if video.pause:
                print("Continuing video: " + video.title)
                found = True
            elif video.playing:
                found = True
                print("Cannot continue video: Video is not paused ")

        if not found:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        found = False
        add = ""

        for video in self.videos_list:
            if video.playing:
                found = True
                if video.pause:
                    add = " - PAUSED"
                print("Currently playing: " + video.title + " (" + str(video.video_id) + ") ""[" + self.extract_tags(
                    video.tags) + "]" + add)

        if not found:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if ' ' in playlist_name:
            print("Cannot create playlist: Whitespace is not allowed")
        elif self.compare_playlist(playlist_name):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists.append(playlist_name)
            self.playlists_tracks.append([])
            print("Successfully created new playlist: " + playlist_name)

    def compare_playlist(self, playlist_name):
        for playlist in self.playlists:
            if playlist.upper() == playlist_name.upper():
                return True
        return False

    def search_id(self, video_id):
        for video in self.videos_list:
            if video.video_id == video_id:
                return True
        return False

    def get_name(self, video_id):
        for video in self.videos_list:
            if video.video_id == video_id:
                return video.title

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if not self.check_playlist(playlist_name):
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        elif not self.search_id(video_id):
            print("Cannot add video to " + playlist_name + ": Video does not exist")
        else:
            for count in range(len(self.playlists)):
                if self.playlists[count].upper() == playlist_name.upper():
                    if video_id in self.playlists_tracks[count]:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                    else:
                        self.playlists_tracks[count].append(video_id)
                        print("Added video to " + playlist_name + ": " + self.get_name(video_id))

    def check_playlist(self, playlist_name):
        for playlist in self.playlists:
            if playlist_name.upper() == playlist.upper():
                return True
        return False


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists) == 0 :
            print("No playlists exist yet.")
        else:
            print("Showing all playlists:")
            for playlist in sorted(self.playlists):
                print(playlist)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.check_playlist(playlist_name):
            print("Showing playlist: " + playlist_name)
            count = 0
            for index, playlist in enumerate(self.playlists):
                if playlist.upper() == playlist_name:
                    count = index
                    break
            if len(self.playlists_tracks[count]) == 0:
                print("No videos here yet")
            for track in self.playlists_tracks[count]:
                print((self.get_name(track) + " (" + str(track) + ") ""[" + self.get_tags(track) + "]"))
        else:
            print("Cannot show " + playlist_name + ": Playlist does not exist")

    def get_tags(self, video_id):
        for video in self.videos_list:
            if video.video_id == video_id:
                return self.extract_tags(video.tags)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        found = False
        search_results = []
        for video in self.videos_list:
            if search_term.upper() in video.title.upper():
                found = True
                search_results.append(
                    video.title + " (" + str(video.video_id) + ") ""[" + self.extract_tags(video.tags) + "]")
        search_results.sort()
        if not found:
            print("No search results for " + search_term)
        else:
            print("Here are the results for " + search_term + ":")
            for count in range(len(search_results)):
                print(str(count+1) + ") " + search_results[count])

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            value = input()
            if value.isdigit():
                value = int(value)
                if not(value > len(search_results) or value <= 0):
                    video = search_results[value-1]
                    self.play_video(self.extract_id(video))


    def extract_id(self,data):
        video_id = ""
        for index in range(len(data)):
            if data[index] == "(":
                index += 1
                while data[index] != ")":
                    video_id += data[index]
                    index += 1
                return video_id
                break


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        found = False
        search_results = []
        for video in self.videos_list:
            if video_tag.upper() in self.extract_tags(video.tags).upper():
                found = True
                search_results.append(
                    video.title + " (" + str(video.video_id) + ") ""[" + self.extract_tags(video.tags) + "]")
        search_results.sort()
        if not found:
            print("No search results for " + video_tag)
        else:
            print("Here are the results for " + video_tag + ":")
            for count in range(len(search_results)):
                print(str(count + 1) + ") " + search_results[count])

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            value = input()
            if value.isdigit():
                value = int(value)
                if not (value > len(search_results) or value <= 0):
                    video = search_results[value - 1]
                    self.play_video(self.extract_id(video))


    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
