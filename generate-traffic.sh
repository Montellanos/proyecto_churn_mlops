#!/bin/sh

apk add --no-cache curl

# Hilo 1: Health Check Inmortal (Siempre manda 3 peticiones cada 10 segundos)
while true; do
    echo "[HEALTH] Launching batch of 3 health checks..."
    for h in 1 2 3; do
        echo "  -> Health Check $h/3"
        curl -s -m 1 -o /dev/null http://python_app:8000/health
    done
    sleep 10
done &

# Hilo 2: Predict Batch Inmortal (Mínimo 3, máximo 10 peticiones aleatorias cada 5 segundos)
while true; do
    # Calcular cantidad aleatoria entre 3 y 10
    # RANDOM % 8 genera un número de 0 a 7. Al sumarle 3, el rango final es de 3 a 10.
    total_predicts=$((3 + RANDOM % 8))
    
    echo "[PREDICT] Launching dynamic batch of $total_predicts requests..."
    
    for i in $(seq 1 $total_predicts); do
        # Decide if this request should be a failure (20% chance)
        # RANDOM % 10 will give a number from 0 to 9.
        # If the number is 0 or 1, it's a failure (2 out of 10, or 20%).
        if [ $((RANDOM % 10)) -lt 2 ]; then
            # FAILURE CASE: cargo_mensual = 0 and reclamos > 0 (Valores dentro de rangos pero incoherentes)
            antiguedad=$((1 + RANDOM % 100))
            cargo_mensual=0.0
            reclamos=$((1 + RANDOM % 49)) # Entre 1 y 50 (cumple le=50 pero falla coherencia)
            echo "  -> Req $i/$total_predicts: FAILURE CASE (antiguedad=$antiguedad, cargo_mensual=$cargo_mensual, reclamos=$reclamos)"
        else
            # SUCCESS CASE: Valores válidos y coherentes
            # Usamos antiguedad > 0 para evitar la regla de cargo_mensual > 900
            antiguedad=$((1 + RANDOM % 119)) 
            # cargo_mensual entre 1.0 y 800.0 (seguro para cualquier antiguedad)
            cargo_mensual_int=$((1 + RANDOM % 799))
            cargo_mensual_dec=$((RANDOM % 100))
            cargo_mensual="${cargo_mensual_int}.${cargo_mensual_dec}"
            # Reclamos debe ser <= 50 para no dar 422 por rango
            reclamos=$((RANDOM % 51)) 
            echo "  -> Req $i/$total_predicts: SUCCESS CASE (antiguedad=$antiguedad, cargo_mensual=$cargo_mensual, reclamos=$reclamos)"
        fi
        
        curl -s -m 1 -o /dev/null -X POST http://python_app:8000/predict \
            -H "Content-Type: application/json" \
            -d "{\"antiguedad\": $antiguedad, \"cargo_mensual\": $cargo_mensual, \"reclamos\": $reclamos}"
    done

    sleep 5
done