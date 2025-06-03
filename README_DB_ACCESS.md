# 🧑‍💻 Connecting to the MySQL Database

This guide explains how to securely connect to the private AWS RDS MySQL instance using a Bastion Host. You may connect via the command line or using MySQL Workbench.

---

## 🛠️ Requirements

You must be on the **NYU campus network** or connected via **NYU VPN**, and have:

- The **Bastion Host public IP**: `54.80.37.147`
- The **RDS endpoint**:  
  `rds-mysql-nyucsmap-re-eng.cq3y0gicg1oa.us-east-1.rds.amazonaws.com`
- The **SSH private key file**:  
  `csmap-tunnel-only-key`
- The **MySQL username**:  
  `csmap_guest`
- The **MySQL password** (provided separately)
- One of the following installed:
  - Terminal + `ssh` + `mysql-client` *(Option 1)*
  - MySQL Workbench *(Option 2)*

---

## 📡 Option 1: SSH Tunnel + MySQL CLI

### Step 1: Start the SSH Tunnel

```bash
ssh -f -N -i /path/to/csmap-bastion-host-key.pem -L 3306:rds-mysql-nyucsmap-re-eng.cq3y0gicg1oa.us-east-1.rds.amazonaws.com:3306 ec2-user@54.80.37.147
```

> Keep this terminal window open to maintain the SSH tunnel.

---

### Step 2: Open a Second Terminal Window

Connect to the database using the MySQL CLI:

```bash
mysql -h 127.0.0.1 -P 3306 -u csmap_guest -p
```

When prompted, enter the password provided to you.

---

## ✅ Example Session

```bash
$ ssh -i csmap-tunnel-only-key -L 3306:rds-mysql-nyucsmap-re-eng.cq3y0gicg1oa.us-east-1.rds.amazonaws.com ec2-user@54.80.37.147
# [Tunnel is now open — leave this window running]

# In another terminal:
$ mysql -h 127.0.0.1 -P 3306 -u csmap_guest -p
Enter password: ********
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 42
Server version: 8.0.x Amazon RDS

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| transcripts_db     |
+--------------------+

mysql> USE transcripts_db;
mysql> SELECT COUNT(*) FROM episodes;
+----------+
| COUNT(*) |
+----------+
|      123 |
+----------+

mysql> exit
Bye
```

---
## 🖥️ Option 2: Connect via MySQL Workbench (connection does not completely work)

If you prefer a graphical interface, you can connect to the database using MySQL Workbench:

1. Open **MySQL Workbench**

2. Click **+** to create a new connection

3. Use the following connection settings:

| Field               | Value                                                       |
|---------------------|-------------------------------------------------------------|
| Connection Name     | `csmap-rds` (or any name)                                   |
| Connection Method   | `Standard TCP/IP over SSH`                                  |
| SSH Hostname        | `54.80.37.147`                                             |
| SSH Username        | `ec2-user`                                                  |
| SSH Key File        | `/path/to/csmap-tunnel-only-key`                       |
| MySQL Hostname      | `rds-mysql-nyucsmap-re-eng.cq3y0gicg1oa.us-east-1.rds.amazonaws.com` |
| MySQL Port          | `3306`                                                      |
| Username            | `csmap_guest`                                               |
| Password            | Enter manually or store in keychain                         |

4. Click **Test Connection**, then **Connect**

> ✅ This will work if you're on NYU’s campus or connected to the NYU VPN.

## 🔐 Security Notes

- This database is **not publicly accessible**
- SSH access is limited to NYU-assigned IP ranges only:
  - `128.122.0.0/16`, `192.76.177.0/24`, `192.86.139.0/24`, `216.165.0.0/18`, `216.165.64.0/18`
- The RDS port (`3306`) is only reachable through the Bastion Host tunnel

---

## 🧯 Troubleshooting

- Check you're on **NYU's network** or connected via **NYU VPN**
- Make sure the `.pem` key has proper permissions:
  ```bash
  chmod 400 your-key.pem
  ```
- If `mysql` is not installed:
  - macOS: `brew install mysql-client`
  - Ubuntu: `sudo apt install mysql-client`
  - Amazon Linux: `sudo yum install mysql`

Still can't connect? Contact me for access support.
