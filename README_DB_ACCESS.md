# 🧑‍💻 Connecting to the MySQL Database

This guide explains how to securely connect to the private AWS RDS MySQL instance using a Bastion Host. You may connect via the command line or using MySQL Workbench.

---

## 🛠️ Requirements

You must have:

- The **Bastion Host public IP**: `<your-bastion-host-ip>`
- The **RDS endpoint**:  
  `<your-rds-endpoint>`
- The **SSH private key file**:  
  `<your-ssh-private-key>`
- The **MySQL username**:  
  `<your-db-username>`
- The **MySQL password** (provided separately)
- One of the following installed:
  - Terminal + `ssh` + `mysql-client` *(Option 1)*
  - MySQL Workbench *(Option 2)*

---

## 📡 Option 1: SSH Tunnel + MySQL CLI

### Step 1: Start the SSH Tunnel

```bash
ssh -f -N -i /path/to/<your-ssh-private-key>.pem -L 3306:<your-rds-endpoint>:3306 <your-ssh-username>@<your-bastion-host-ip>

```

> Keep this terminal window open to maintain the SSH tunnel.

---

### Step 2: Open a Second Terminal Window

Connect to the database using the MySQL CLI:

```bash
mysql -h 127.0.0.1 -P 3306 -u <your-db-username> -p
```

When prompted, enter the password provided to you.

---

## ✅ Example Session

```bash
$ ssh -i <your-ssh-private-key> -L 3306:<your-rds-endpoint>:3306 <your-ssh-username>@<your-bastion-host-ip>
# [Tunnel is now open — leave this window running]

# In another terminal:
$ mysql -h 127.0.0.1 -P 3306 -u <your-db-username> -p
Enter password: ********
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 42
Server version: 8.0.x Amazon RDS

mysql> SHOW DATABASES;
+----------------------+
| Database             |
+----------------------+
| information_schema   |
| <your-database-name> |
+----------------------+

mysql> USE <your-database-name>;
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
## 🖥️ Option 2: Connect via MySQL Workbench

If you prefer a graphical interface, you can connect to the database using MySQL Workbench:

1. Open **MySQL Workbench**

2. Click **+** to create a new connection

3. Use the following connection settings:

| Field             | Value                          |
|-------------------|----------------------------------|
| Connection Name   | `<your-connection-name>`        |
| Connection Method | `Standard TCP/IP over SSH`      |
| SSH Hostname      | `<your-bastion-host-ip>`        |
| SSH Username      | `<your-ssh-username>`           |
| SSH Key File      | `/path/to/<your-ssh-private-key>` |
| MySQL Hostname    | `<your-rds-endpoint>`           |
| MySQL Port        | `3306`                          |
| Username          | `<your-db-username>`            |
| Password          | Enter manually or store in keychain |

4. Click **Test Connection**, then **Connect**

> ✅ This assumes the SSH tunnel is properly configured.

---

## 🔐 Security Notes

- This database is **not publicly accessible**
- SSH access is restricted to authorized users only.
- The RDS port (`3306`) is only reachable through the Bastion Host tunnel.

---

## 🧯 Troubleshooting

- Verify you are on the authorized network or VPN (if applicable).
- Ensure your SSH private key file has correct permissions:
  ```bash
  chmod 400 your-key.pem
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

