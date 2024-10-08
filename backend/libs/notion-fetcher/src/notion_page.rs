use std::collections::HashMap;

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Number;

/// Properties common on all rich text objects
/// See <https://developers.notion.com/reference/rich-text#all-rich-text>
#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
pub struct RichTextCommon {
    pub plain_text: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub href: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub annotations: Option<Annotations>,
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum RichText {
    /// See <https://developers.notion.com/reference/rich-text#text-objects>
    Text {
        #[serde(flatten)]
        rich_text: RichTextCommon,
        text: Text,
    },
    /// See <https://developers.notion.com/reference/rich-text#mention-objects>
    Mention {
        #[serde(flatten)]
        rich_text: RichTextCommon,
        mention: MentionObject,
    },
    /// See <https://developers.notion.com/reference/rich-text#equation-objects>
    Equation {
        #[serde(flatten)]
        rich_text: RichTextCommon,
    },
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum PropertyValue {
    // <https://developers.notion.com/reference/property-object#title-configuration>
    Title {
        id: uuid::Uuid,
        title: Vec<RichText>,
    },
    /// <https://developers.notion.com/reference/property-object#text-configuration>
    #[serde(rename = "rich_text")]
    Text {
        id: uuid::Uuid,
        rich_text: Vec<RichText>,
    },
    /// <https://developers.notion.com/reference/property-object#number-configuration>
    Number {
        id: uuid::Uuid,
        number: Option<Number>,
    },
    /// <https://developers.notion.com/reference/property-object#select-configuration>
    Select {
        id: uuid::Uuid,
        select: Option<SelectedValue>,
    },
    /// <https://developers.notion.com/reference/property-object#status-configuration>
    Status {
        id: uuid::Uuid,
        status: Option<SelectedValue>,
    },
    /// <https://developers.notion.com/reference/property-object#multi-select-configuration>
    MultiSelect {
        id: uuid::Uuid,
        multi_select: Option<Vec<SelectedValue>>,
    },
    /// <https://developers.notion.com/reference/property-object#date-configuration>
    Date {
        id: uuid::Uuid,
        date: Option<DateValue>,
    },
    /// <https://developers.notion.com/reference/property-object#formula-configuration>
    Formula {
        id: uuid::Uuid,
        formula: FormulaResultValue,
    },
    /// <https://developers.notion.com/reference/property-object#relation-configuration>
    /// It is actually an array of relations
    Relation {
        id: uuid::Uuid,
        relation: Option<Vec<RelationValue>>,
    },
    /// <https://developers.notion.com/reference/property-object#rollup-configuration>
    Rollup {
        id: uuid::Uuid,
        rollup: Option<RollupValue>,
    },
    /// <https://developers.notion.com/reference/property-object#people-configuration>
    People {
        id: uuid::Uuid,
        people: Vec<User>,
    },
    /// <https://developers.notion.com/reference/property-object#files-configuration>
    Files {
        id: uuid::Uuid,
        files: Option<Vec<FileReference>>,
    },
    /// <https://developers.notion.com/reference/property-object#checkbox-configuration>
    Checkbox {
        id: uuid::Uuid,
        checkbox: bool,
    },
    /// <https://developers.notion.com/reference/property-object#url-configuration>
    Url {
        id: uuid::Uuid,
        url: Option<String>,
    },
    /// <https://developers.notion.com/reference/property-object#email-configuration>
    Email {
        id: uuid::Uuid,
        email: Option<String>,
    },
    /// <https://developers.notion.com/reference/property-object#phone-number-configuration>
    PhoneNumber {
        id: uuid::Uuid,
        phone_number: String,
    },
    /// <https://developers.notion.com/reference/property-object#created-time-configuration>
    CreatedTime {
        id: uuid::Uuid,
        created_time: DateTime<Utc>,
    },
    /// <https://developers.notion.com/reference/property-object#created-by-configuration>
    CreatedBy {
        id: uuid::Uuid,
        created_by: User,
    },
    /// <https://developers.notion.com/reference/property-object#last-edited-time-configuration>
    LastEditedTime {
        id: uuid::Uuid,
        last_edited_time: DateTime<Utc>,
    },
    /// <https://developers.notion.com/reference/property-object#last-edited-by-configuration>
    LastEditedBy {
        id: uuid::Uuid,
        last_edited_by: User,
    },
    UniqueId {
        id: uuid::Uuid,
        unique_id: UniqueidValue,
    },
    Button {
        id: uuid::Uuid,
    },
}
#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
pub struct Properties {
    #[serde(flatten)]
    pub properties: HashMap<String, PropertyValue>,
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum Parent {
    #[serde(rename = "database_id")]
    Database {
        database_id: uuid::Uuid,
    },
    #[serde(rename = "page_id")]
    Page {
        page_id: uuid::Uuid,
    },
    Workspace,
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum IconObject {
    File {
        #[serde(flatten)]
        file: FileObject,
    },
    External {
        external: ExternalFileObject,
    },
    Emoji {
        emoji: String,
    },
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub struct Cover {
    url: String,
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
pub struct Cover {
    url: String,
}

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
pub struct NotionPage {
    pub id: uuid::Uuid,
    pub created_time: DateTime<Utc>,
    /// Date and time when this page was updated.
    pub last_edited_time: DateTime<Utc>,
    pub archived: bool,
    pub in_trash: bool,
    pub properties: Properties,
    pub cover: Option<Cover>,
    pub icon: Option<IconObject>,
    pub parent: Parent,
}
