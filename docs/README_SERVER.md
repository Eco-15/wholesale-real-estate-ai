# Web Server Setup

## Quick Start

Start the web server:
```bash
python3 server.py
```

Then open your browser to: **http://localhost:8000**

## How It Works

The web server provides a live dashboard that automatically shows the latest data. Unlike the standalone HTML file, you don't need to manually open files each time.

### Workflow

1. **Start the server** (only once):
   ```bash
   python3 server.py
   ```

2. **Keep your browser open** to http://localhost:8000

3. **When you want fresh data**, run:
   ```bash
   ./refresh_data.sh
   ```

4. **Refresh your browser** (F5 or Cmd+R) to see the new data

## Features

### Main Dashboard
- **URL**: http://localhost:8000
- Shows the complete dashboard with all filters and tabs
- Automatically uses the latest CSV data files

### API Endpoints

**Get Fresh Data (JSON)**
```bash
curl http://localhost:8000/api/data
```

**Trigger Full Refresh**
```bash
curl http://localhost:8000/api/refresh
```

## Comparison: Server vs Static HTML

### Web Server Method (Recommended)
- **Start**: `python3 server.py`
- **URL**: http://localhost:8000
- **Refresh Data**: `./refresh_data.sh` then refresh browser
- **Benefits**: Live updates, API access, cleaner workflow

### Static HTML Method
- **Generate**: `./refresh_dashboard.sh`
- **Open**: `open opportunities_dashboard.html`
- **Refresh Data**: Run script again, file reopens
- **Benefits**: Works offline, no server needed

## Stopping the Server

Press `Ctrl+C` in the terminal where server.py is running.

## Troubleshooting

**Port 5000 already in use?**
- The server uses port 8000 by default (avoiding AirPlay on macOS)
- To change: Edit `server.py` and modify the port number

**Data not updating?**
1. Make sure you ran `./refresh_data.sh`
2. Refresh your browser (Cmd+R or F5)
3. Check the terminal for errors

**Server won't start?**
- Make sure Flask is installed: `pip3 install flask`
- Check if another process is using port 8000

## Scripts Overview

- `server.py` - Web server for live dashboard
- `refresh_data.sh` - Regenerate data without opening browser
- `refresh_dashboard.sh` - Regenerate data and open HTML file (old method)

## Advanced Usage

### Run on Different Port
Edit `server.py`, line 133:
```python
app.run(debug=True, host='0.0.0.0', port=9000)  # Change to any port
```

### Access From Other Devices
The server runs on all network interfaces (0.0.0.0), so you can access it from:
- Your phone: http://YOUR_IP:8000
- Another computer: http://YOUR_IP:8000

Find your IP by running: `ifconfig | grep "inet "`
