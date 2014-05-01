TCC Database Manager
====================

Apple manages access to certain services, such as the Address Book, Accessibility, and iCloud, through a couple SQL databases on the computer.  These databases are named 'TCC.db', and the purpose of this script is to help administrators to manage these databases manually.

## Contents

* [History](#history) - why this script exists
  * [Problems](#problems)
  * [Solutions](#solutions)
* [Usage](#usage) - how to use the script
  * [Options](#options)
  * [Actions](#actions)
  * [Services](#services)
  * [Applications](#applications)
* [Location Services](#location-services) - relation to Location Services
* [Grievances](#greivances) - difficulties with the TCC system at-large
* [Technical](#technical) - behind-the-scenes explanations
* [Attribution](#attribution) - thanks!

## History

With Mac OS X 10.8 "Mountain Lion", Apple introduced a feature which notifies users whenever an application attempts to gain access to their contacts or the computer's "Accessibility" options.  Whenever a user responds to one of these prompts, the computer stores the answer in a database.  In a single-user environment, this doesn't really cause problems.

### Problems

Unfortunately, this system *does* cause issues in managed distributed environments where applicatinos may be added or removed at any time, and the database files would nee dto be updated.  Constantly having to update this file for the template user would be tedious and could cause errors: what if you forgot to add one of the new applications?

### Solution

This script allows applications to be added and removed from the TCC databases during our regular maintenance cycle.  Changes take effect immediately.

## Usage

The script has a few options:

```
$ tcc_database_manager [-hvn] [-l log] [-u user] {action} {service} {applications}
```

### Options

| Option | Purpose |
|--------|---------|
| `-h`, `--help` | Prints usage instructions. |
| `-v`, `--version` | Print current version information. |
| `-n`, `--no-log` | Prevents the program from logging.  All information that would have gone to the logs will be output to console instead. |
| `-l log`, `--log log` | Use `log` as the logging output location. |
| `-u user`, --user user` | Change settings for the user `user`.  This requires elevated permissions. |

### Actions

There are two actions available:

* `add` will insert the specified applications into the appropriate database file.
* `remove` will remove the applications.

### Services

There are three recognized services:

* `contacts`: also called "Address Book"; this handles requests to access your contact information.
* `icloud`: also called "Ubiquity"; this allows applications access to iCloud (though so far only Apple applications use this, so you probably don't need it).
* `accessibility`: allows applications greater control over your computer.  Modifying this service requires root privileges.

### Applications

There are three ways to specify applications:

1. By path to the `.app` folder, e.g. `/Applications/Safari.app`, `/Longer/Path/To/MyApp.app`
2. By bundle identifier, e.g. `com.apple.Safari`, `com.me.myapp`
3. By shortname as it would be found by Spotlight, e.g. `safari`, `myapp`

You may specify as many applications at runtime as you like.  Be careful, though, as they will all be added or removed to the same service.  You may also mix-and-match naming conventions, that is you could do:

```
$ tcc_database_manager add contacts safari /Longer/Path/To/MyApp.app com.apple.TextEdit
```

This would add all three of Safari, MyApp, and TextEdit to the contacts service for the current user.

## Location Services

Although it may seem that Location Services would fit into the same category as these services, Apple does not handle its Location Services requests through the TCC database system.  Instead it is handled through some plists - see [Location Services Manager](https://github.com/univ-of-utah-marriott-library-apple/location_services_manager).

## Grievances

Unfortunately, there does not seem to be an easy way to simply find out whether an application will request access to one of these services without opening the application and navigating it to a point where it asks for permission (the [Halting Problem](http://en.wikipedia.org/wiki/Halting_problem)).  We have been investigating methods of programmatically discerning which of our applications will prompt the user to access different services, but have thus far been unsuccessful.  If you happen to know anything about this, we'd greatly appreciate any ideas.

It is worth noting that Apple has a method of automatically allowing certain applications access to services.  For example, in Mac OS X 10.9 "Mavericks", TextEdit will automatically gain access to the `kTCCServiceUbiquity` service during its first launch, without any sort of prompt to the user.  We contacted Apple about utilizing this apparent backdoor for our machines so that we could just allow all requests to Contacts access (which would not pose an issue in our environment, I promise), but they informed us that this ability is hardcoded into the OS and we cannot access it.

There is also the mysterious `tccutil` command.  Its man page states:
```
DESCRIPTION
     The tccutil command manages the privacy database, which stores decisions the user has made about whether apps may
     access personal data.

     One command is current supported:

     reset    Reset all decisions for the specified service, causing apps to prompt again the next time they access the ser-
              vice.
```
I wish that this utility could be used to add access to a particular service for a specified application, or to completely open a service up and automatically accept all requests to it, or to turn off the service entirely so requests don't even exist... but none of this is possible.  The command only resets all access requests to a given service.

## Technical

Apple in fact has multiple TCC.db database files in any given installation of OS X 10.8 or newer (though none of them exist until the appropriate service is requested access to).  There is one for each user, in their `~/Library/Application Support/com.apple.TCC` folder, and there is one root database, located in `/Library/Application Support/com.apple.TCC`.  The local databases (those in each user's directory) are responsible for Contacts access and iCloud access.  The settings for these applications are granted on a per-user, per-application basis this way.  However, Accessibility permissions are stored (and must be stored) in the `/Library/...` database.  I assume this is due to the nature of those types of applications that request Accessibility access (they are granted some freedoms to the machine that could potentially be undesirable, so administrative access is required to add them).

This script will add Accessibility requests to the `/Library/...` database (assuming it is run with root permissions).  The other requests will be added to the TCC database file located at `~/Library/Application Support/com.apple.TCC/TCC.db`.  This is Apple's default directory for an individual user's settings.

## Attribution

Much of the code used in this script was copy/pasted and then adapted from the `tccmanager.py` script written by Tim Sutton and published to his [GitHub repository](http://github.com/timsutton/scripts/tree/master/tccmanager).  We're very grateful to Tim for posting his code online freely; it has been very helpful to us.
