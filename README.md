Tool for synchronizing VLANs between Cisco devices and a DB

### Done items:

- load configuration setting from vlan_sync_cfg.yml
- have 2 loggers: poller and db
- user/pass credentials to be supplied as environment variables: USERNAME, PASSWORD
- It can load inventory from inventory.yml file and from remote sources (not implemented yet)
- As ORM it is using SQLAlchemy with an in-memory database for testing the script
- I'm using Netmiko. Scrapli and pyATS/Genie are too big to install just this test/tool


### Pending items:
- Only with 2 items is not possible to identify what is new and what is deleted, between 
  different runs of the tool
- One option is to rely in a SoT to enforce VLANs accoding the DB
- Another option to achieve consistency without a Single Source of Truth (SoT), is to add
  a 3rd item, a previous VLANs in the device, with another table in the DB
  And so we will be comparing
  - previous VLANs in device
  - current VLANs in device
  - VLANs in DB general table 
- From there take the decision where to apply the add/mod/delete
- Testings are not complete. Just started
