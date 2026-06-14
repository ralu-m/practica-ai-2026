#!/bin/bash

DIRECTOR_SURSĂ="$HOME/documente"
DIRECTOR_BACKUP="$HOME/backup-uri"
LOG_FILE="$HOME/backup_monitor.log"
MAX_BACKUP_URI=7
ALERT_CPU=80
ALERT_MEM=90
ALERT_DISK=85


log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}


monitorizeaza_sistem() {
    log "📊 MONITORIZARE SISTEM:"

    LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | tr -d ' ')
    CORI=$(nproc)
    PROCENT_CPU=$(echo "scale=0; $LOAD * 100 / $CORI" | bc)
    log "  CPU Load: $LOAD (${PROCENT_CPU}% din $CORI core-uri)"
    if [ "$PROCENT_CPU" -gt "$ALERT_CPU" ]; then
        log "  ⚠️  ALERTĂ CPU: $PROCENT_CPU% > ${ALERT_CPU}%"
    fi

    MEM_TOTAL=$(free -m | awk '/^Mem:/{print $2}')
    MEM_FOLOSIT=$(free -m | awk '/^Mem:/{print $3}')
    PROCENT_MEM=$(( MEM_FOLOSIT * 100 / MEM_TOTAL ))
    log "  RAM: ${MEM_FOLOSIT}MB / ${MEM_TOTAL}MB (${PROCENT_MEM}%)"
    if [ "$PROCENT_MEM" -gt "$ALERT_MEM" ]; then
        log "  ⚠️  ALERTĂ MEMORIE: $PROCENT_MEM% > ${ALERT_MEM}%"
    fi

    DISK_FOLOSIT=$(df / | awk 'NR==2{print $5}' | tr -d '%')
    log "  Disc: folosit ${DISK_FOLOSIT}%"
    if [ "$DISK_FOLOSIT" -gt "$ALERT_DISK" ]; then
        log "  ⚠️  ALERTĂ DISC: ${DISK_FOLOSIT}% > ${ALERT_DISK}%"
    fi

    log "  🔥 Top 3 procese după CPU:"
    ps aux --sort=-%cpu | head -4 | tail -3 | while read line; do
        log "    $line"
    done

    echo "" >> "$LOG_FILE"
}


fa_backup() {
    TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
    NUME_BACKUP="backup_${TIMESTAMP}.tar.gz"
    CALE_BACKUP="${DIRECTOR_BACKUP}/${NUME_BACKUP}"

    if [ ! -d "$DIRECTOR_SURSĂ" ]; then
        log "❌ Directorul sursă nu există: $DIRECTOR_SURSĂ"
        return 1
    fi

    mkdir -p "$DIRECTOR_BACKUP"

    log "📦 BACKUP: $DIRECTOR_SURSĂ → $CALE_BACKUP"

    tar -czf "$CALE_BACKUP" -C "$(dirname $DIRECTOR_SURSĂ)" "$(basename $DIRECTOR_SURSĂ)" 2>> "$LOG_FILE"

    if [ $? -eq 0 ]; then
        MARIME=$(du -h "$CALE_BACKUP" | cut -f1)
        log "✅ Backup reușit! Mărime: $MARIME"
    else
        log "❌ Backup eșuat!"
        return 1
    fi

    NR_BACKUP_URI=$(ls -1 "$DIRECTOR_BACKUP"/backup_*.tar.gz 2>/dev/null | wc -l)
    if [ "$NR_BACKUP_URI" -gt "$MAX_BACKUP_URI" ]; then
        log "🧹 Rotire: păstrăm ultimele $MAX_BACKUP_URI backup-uri..."
        ls -1t "$DIRECTOR_BACKUP"/backup_*.tar.gz | tail -n +$((MAX_BACKUP_URI + 1)) | while read F; do
            rm -f "$F"
            log "  Șters: $(basename $F)"
        done
    fi
}


echo ""
log "========================================"
log "🚀 START Backup & Monitorizare"
log "========================================"

monitorizeaza_sistem

fa_backup

log "========================================"
log "✅ FINALIZAT"
log "========================================"
echo ""
