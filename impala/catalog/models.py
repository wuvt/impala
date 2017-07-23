from impala import db
from sqlalchemy.dialects.postgresql import UUID
import enum


class Stack(db.Model):
    __tablename__ = 'stacks'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text())

    holding_groups = db.relationship("HoldingGroup", backref="stack",
                                     lazy="dynamic")


class Format(db.Model):
    __tablename__ = 'formats'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text())
    physical = db.Column(db.Boolean(), nullable=False)

    holdings = db.relationship("Holding", backref="format", lazy="dynamic")


class HoldingGroup(db.Model):
    __tablename__ = 'holding_groups'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    album_title = db.Column(db.String(), nullable=False)
    album_artist = db.Column(db.String(), nullable=False)
    releasegroup_mbid = db.Column(UUID)
    description = db.Column(db.Text())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    stack_id = db.Column(UUID, db.ForeignKey('stacks.id'), nullable=False)
    holdings = db.relationship("Holding", backref="holding_group",
                               lazy="dynamic")

    def __repr__(self):
        return "{} by {} <{}>".format(self.album_title, self.album_artist,
                                      self.id)


class Holding(db.Model):
    __tablename__ = 'holdings'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    label = db.Column(db.String())
    release_mbid = db.Column(UUID)
    description = db.Column(db.Text())
    source_url = db.Column(db.String())
    source_desc = db.Column(db.Text())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    holding_group_id = db.Column(UUID, db.ForeignKey('holding_groups.id'),
                                 nullable=False)
    format_id = db.Column(UUID, db.ForeignKey('formats.id'), nullable=False)
    rotation_releases = db.relationship("RotationRelease", backref="holding",
                                        lazy="dynamic")
    holding_tags = db.relationship("HoldingTag", backref="holding",
                                   lazy="dynamic")
    holding_comments = db.relationship("HoldingComment", backref="holding",
                                       lazy="dynamic")
    tracks = db.relationship("Track", backref="holding", lazy="dynamic")

    def __repr__(self):
        return "{} by {} on {} ({}) <{}>".format(self.holding_group.album_title,
                                                 self.holding_group.album_artist,
                                                 self.label, self.format.name,
                                                 self.id)


class RotationRelease(db.Model):
    __tablename__ = 'rotation_releases'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    start = db.Column(db.DateTime(), nullable=False)
    stop = db.Column(db.DateTime())
    bin = db.Column(db.String())

    holding_id = db.Column(UUID, db.ForeignKey('holdings.id'), nullable=False)


class HoldingTag(db.Model):
    __tablename__ = 'holding_tags'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    owner = db.Column(db.String())
    tag = db.Column(db.String(), nullable=False)

    holding_id = db.Column(UUID, db.ForeignKey('holdings.id'), nullable=False)


class HoldingCommentType(enum.Enum):
    REVIEW = "Review"
    COMMENT = "Comment"
    TRACK_WARNING = "Track warning"
    OTHER = "Other"


class HoldingComment(db.Model):
    __tablename__ = 'holding_comments'

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    comment_text = db.Column(db.Text())
    reviewer_username = db.Column(db.String())
    reviewer_fullname = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer())
    review_date = db.Column(db.Date())
    type = db.Column(db.Enum(HoldingCommentType),
                     default=HoldingCommentType.OTHER, nullable=False)

    holding_id = db.Column(UUID, db.ForeignKey('holdings.id'), nullable=False)


class TrackFccStatus(enum.Enum):
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    title = db.Column(db.String(), nullable=False)
    artist = db.Column(db.String(), nullable=False)
    file_path = db.Column(db.String())
    track_num = db.Column(db.Integer(), nullable=False)
    disc_num = db.Column(db.Integer(), nullable=False, default=1)
    track_mbid = db.Column(UUID)
    recording_mbid = db.Column(UUID)
    has_fcc = db.Column(db.Enum(TrackFccStatus), nullable=False,
                        default=TrackFccStatus.UNKNOWN)

    holding_id = db.Column(UUID, db.ForeignKey('holdings.id'), nullable=False)
    track_metadata = db.relationship("TrackMetadata", backref="track",
                                     lazy="dynamic")


class TrackMetadata(db.Model):
    __tablename__ = "track_metadata"

    id = db.Column(UUID, primary_key=True)
    added_by = db.Column(db.String(), nullable=False)
    added_at = db.Column(db.DateTime(), nullable=False)

    key = db.Column(db.String(), nullable=False)
    value = db.Column(db.Text(), nullable=False)

    track_id = db.Column(UUID, db.ForeignKey('tracks.id'), nullable=False)
