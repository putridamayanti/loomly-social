from typing import Optional

from app.models.media_model import Media


class MediaRepository:
    def __init__(self, db):
        self.db = db
        self.model = Media

    def get_media_by_id(self, media_id):
        return self.db.query(self.model).filter(Media.id == media_id).first()

    def create_media(self, media_data):
        new_media = Media(**media_data)
        self.db.add(new_media)
        self.db.commit()
        self.db.refresh(new_media)
        return new_media

    def update_media(self, media_id, media_data):
        media = self.get_media_by_id(media_id)
        if not media:
            return None
        for key, value in media_data.items():
            setattr(media, key, value)
        self.db.commit()
        self.db.refresh(media)
        return media

    def delete_media(self, media_id):
        media = self.get_media_by_id(media_id)
        if not media:
            return None
        self.db.delete(media)
        self.db.commit()
        return media