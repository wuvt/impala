package main

import (
	"context"
	"database/sql/driver"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/uptrace/bun"
)

type App struct {
	Ctx   context.Context
	Flags Flags

	DB *bun.DB
}

type Flags struct {
	ConnectionString string
	Port             uint16
}

type Stack struct {
	Id          uuid.UUID `bun:"type:uuid,pk"`
	AddedBy     string    `bun:",notnull"`
	AddedAt     time.Time `bun:"type:timestamp,notnull"`
	Name        string    `bun:",notnull"`
	Description string    `bun:"type:text"`
}

type Format struct {
	Id          uuid.UUID `bun:"type:uuid,pk"`
	AddedBy     string    `bun:",notnull"`
	AddedAt     time.Time `bun:"type:timestamp,notnull"`
	Name        string    `bun:",notnull"`
	Description string    `bun:"type:text"`
	Physical    bool      `bun:",notnull"`
}

type HoldingGroup struct {
	Id          uuid.UUID `bun:"type:uuid,pk"`
	AddedBy     string    `bun:",notnull"`
	AddedAt     time.Time `bun:"type:timestamp,notnull"`
	AlbumTitle  string    `bun:",notnull"`
	AlbumArtist string    `bun:",notnull"`
	MBId        uuid.UUID `bun:"releasegroup_mbid,type:uuid"`
	Description string    `bun:"type:text"`
	Active      bool      `bun:",notnull"`
	StackId     uuid.UUID `bun:"type:uuid,notnull"`
	Stack       Stack     `bun:"rel:has-one,join:stack_id=id"`
}

type Holding struct {
	Id             uuid.UUID `bun:"type:uuid,pk"`
	AddedBy        string    `bun:",notnull"`
	AddedAt        time.Time `bun:"type:timestamp,notnull"`
	Label          string
	MBId           uuid.UUID `bun:"releasegroup_mbid,type:uuid"`
	Description    string    `bun:"type:text"`
	SourceURL      string
	SourceDesc     string       `bun:"type:text"`
	TorrentHash    string       `bun:",unique"`
	Active         bool         `bun:",notnull"`
	HoldingGroupId uuid.UUID    `bun:"type:uuid,notnull"`
	HoldingGroup   HoldingGroup `bun:"rel:has-one,join:holding_group_id=id"`
	FormatId       uuid.UUID    `bun:"type:uuid,notnull"`
	Format         Format       `bun:"rel:has-one,join:format_id=id"`
}

type RotationRelease struct {
	Id        uuid.UUID `bun:"type:uuid,pk"`
	AddedBy   string    `bun:",notnull"`
	AddedAt   time.Time `bun:"type:timestamp,notnull"`
	Start     time.Time `bun:"type:timestamp,notnull"`
	Stop      time.Time `bun:"type:timestamp"`
	Bin       string
	HoldingId uuid.UUID `bun:"type:uuid,notnull"`
	Holding   Holding   `bun:"rel:has-one,join:holding_id=id"`
}

type HoldingTag struct {
	Id        uuid.UUID `bun:"type:uuid,pk"`
	AddedBy   string    `bun:",notnull"`
	AddedAt   time.Time `bun:"type:timestamp,notnull"`
	Owner     string
	Tag       string    `bun:",notnull"`
	HoldingId uuid.UUID `bun:"type:uuid,notnull"`
	Holding   Holding   `bun:"rel:has-one,join:holding_id=id"`
}

type HoldingCommentType string

const (
	holdingReview  HoldingCommentType = "REVIEW"
	holdingComment HoldingCommentType = "COMMENT"
	holdingWarning HoldingCommentType = "TRACK_WARNING"
	holdingOther   HoldingCommentType = "OTHER"
)

func (c HoldingCommentType) Value() (driver.Value, error) {
	return string(c), nil
}

func (c *HoldingCommentType) Scan(src interface{}) error {
	var value string
	switch src := src.(type) {
	case string:
		value = src
	case []byte:
		value = string(src)
	case nil:
		value = "OTHER"
	default:
		return fmt.Errorf("unsupported data type: %T", src)
	}

	if value == "REVIEW" || value == "COMMENT" || value == "TRACK_WARNING" || value == "OTHER" {
		*c = HoldingCommentType(value)
		return nil
	} else {
		return fmt.Errorf("invalid holding comment type: %s", value)
	}
}

type HoldingComment struct {
	Id               uuid.UUID `bun:"type:uuid,pk"`
	AddedBy          string    `bun:",notnull"`
	AddedAt          time.Time `bun:"type:timestamp,notnull"`
	CommentText      string    `bun:"type:text"`
	ReviewerUsername string
	ReviewerFullname string             `bun:",notnull"`
	Rating           int                `bun:"type:integer"`
	ReviewDate       time.Time          `bun:"type:date"`
	Type             HoldingCommentType `bun:"type:holdingcommenttype,notnull"`
	HoldingId        uuid.UUID          `bun:"type:uuid,notnull"`
	Holding          Holding            `bun:"rel:has-one,join:holding_id=id"`
}

type TrackFccStatus string

const (
	trackFccYes     TrackFccStatus = "YES"
	trackFccNo      TrackFccStatus = "NO"
	trackFccUnknown TrackFccStatus = "UNKNOWN"
)

func (c TrackFccStatus) Value() (driver.Value, error) {
	return string(c), nil
}

func (s *TrackFccStatus) Scan(src interface{}) error {
	var value string
	switch src := src.(type) {
	case string:
		value = src
	case []byte:
		value = string(src)
	case nil:
		value = "UNKNOWN"
	default:
		return fmt.Errorf("unsupported data type: %T", src)
	}

	if value == "YES" || value == "NO" || value == "UNKNOWN" {
		*s = TrackFccStatus(value)
		return nil
	} else {
		return fmt.Errorf("invalid track fcc status: %s", value)
	}
}

type Track struct {
	Id            uuid.UUID `bun:"type:uuid,pk"`
	AddedBy       string    `bun:",notnull"`
	AddedAt       time.Time `bun:"type:timestamp,notnull"`
	Title         string    `bun:",notnull"`
	Artist        string    `bun:",notnull"`
	FilePath      string
	TrackNum      int            `bun:"type:integer,notnull"`
	DiscNumber    int            `bun:"type:integer,notnull"`
	TrackMBId     uuid.UUID      `bun:"track_mbid,type:uuid"`
	RecordingMBId uuid.UUID      `bun:"recording_mbid,type:uuid"`
	HasFcc        TrackFccStatus `bun:"type:trackfccstatus,notnull"`
	HoldingId     uuid.UUID      `bun:"type:uuid,notnull"`
	Holding       Holding        `bun:"rel:has-one,join:holding_id=id"`
}

type TrackMetadata struct {
	Id      uuid.UUID `bun:"type:uuid,pk"`
	AddedBy string    `bun:",notnull"`
	AddedAt time.Time `bun:"type:timestamp,notnull"`
	Key     string    `bun:",notnull"`
	Value   string    `bun:"type:text,notnull"`
	TrackId uuid.UUID `bun:"type:uuid,notnull"`
	Track   Track     `bun:"rel:has-one,join:track_id=id"`
}
