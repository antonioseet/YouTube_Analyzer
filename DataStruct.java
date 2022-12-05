import java.util.HashMap;

class VideoData{
    String video_id, uploader, category;
    int age, length, views, ratings, comments;
    double rate;
    String[] relatedVideoIds;
}

class VideoManager{
    HashMap<String, VideoData> videoMap = new HashMap<String, VideoData>();;
}