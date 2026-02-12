@app.post("/api/rating")
async def save_rating(data: RatingRequest):
    """
    Guarda una nueva calificación. Vincula cliente si existe.
    """
    table_calif = get_table("CALIFICACIONES")
    table_clientes = get_table("CLIENTES")
    
    if not table_calif:
        raise HTTPException(status_code=500, detail="Airtable config missing")

    # Campos base
    fields = {
        "ESTRELLAS": data.estrellas,
        "CUAL FUE TU EXPERIENCIA CON NOSOTROS": data.estrellas, 
        "NOMBRE": data.nombre,
        "ES_CLIENTE": data.es_cliente,
        "SERVICIO": data.servicio,
        "COMENTARIO": data.comentario,
        "MODO": "Online",
        "VISIBLE": True,
        "AUTORIZA_PUBLICAR": data.autoriza_publicar,
        "USAR FOTO": data.usar_foto,
        "EMPLEADO": ["recrUCS6NhFjVmzqm"] # ID Agente Online
    }

    client_linked = False
    
    # Intentar vincular cliente
    if data.es_cliente == "Sí" and data.dni:
        # Por defecto asumimos 'No' hasta encontrarlo (Lógica N8N)
        fields["ES_CLIENTE"] = "No" 
        
        if table_clientes:
            # Buscar ID del cliente
            formula = f"{{DNI}}='{data.dni}'"
            c_records = table_clientes.all(formula=formula, max_records=1)
            
            if c_records:
                fields["CLIENTE"] = [c_records[0]["id"]]  # Link record
                fields["ES_CLIENTE"] = "Sí"  # Confirmado
                fields["DNI"] = data.dni
                client_linked = True
            else:
                # No encontrado -> Se mantiene ES_CLIENTE='No' y sin DNI vinculado
                pass
    
    try:
        record = table_calif.create(fields)
        return {
            "status": "success",
            "message": "Calificación registrada correctamente",
            "recordId": record["id"],
            "clienteVinculado": client_linked
        }
    except Exception as e:
        print(f"Error creando rating: {e}")
        raise HTTPException(status_code=500, detail=str(e))