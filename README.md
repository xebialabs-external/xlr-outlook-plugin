# Outlook Plugin for Digital.ai Release

This Plugin has a Task that sends out an iCalendar invite. Compatible with at least Microsoft Outlook and Gmail.

### Building the plugin

`./gradlew clean build`

### Server Configuration

- Title. The name by which you will be referring to this Mail Server.

#### Input
- Username. Your Mail Server Username.
- Password or Token. Your Mail Server Password or Token associated with the Username.

## Tasks

### Send Invite
This Task sends an iCalendar invite.

#### Input parameters
- Server. The corresponding Outlook/Mail Server.
- Emails. A list of comma-separated email addresses - recipients of the iCalendar invite. Example: "user1@company.com, user2@company.com, user3@company.com".
- Event Start Time. The start time of the event (Eastern Time): MM/DD/YY hh:mm (08/15/21 17:30).
- Event End Time. The end time of the event (Eastern Time): MM/DD/YY hh:mm (08/15/21 21:30).
- Event Subject. The title of the event. Example: "Maintenance Window".
- Event Message. The body of the iCalendar event. Example: "Hello everyone! This is the upcoming Maintenance Window.".
- Sender. Email address of the sender (associated with the Username): "username@company.com".