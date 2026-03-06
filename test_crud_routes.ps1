# Script para probar todas las rutas CRUD
# Ejecutar en PowerShell después de que Flask esté corriendo

# ============ PRUEBAS CRUD PARA CONTACTOS ============

# 1. POST - Crear un nuevo contacto
$body_crear = @{
  nombre = "Carlos García"
  correo = "carlos@example.com"
  mensaje = "Tengo una consulta sobre el programa"
} | ConvertTo-Json

Write-Host "1. POST /api/contactos - Crear nuevo contacto" -ForegroundColor Green
$r1 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos" -Method POST -Body $body_crear -ContentType "application/json"
$r1.StatusCode
Start-Sleep -Milliseconds 500


# 2. GET - Obtener todos los contactos
Write-Host "`n2. GET /api/contactos - Obtener todos los contactos" -ForegroundColor Green
$r2 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos" -Method GET
$r2.StatusCode
$datos2 = $r2.Content | ConvertFrom-Json
Write-Host "Total contactos: $($datos2.total)"
Start-Sleep -Milliseconds 500


# 3. POST - Crear segundo contacto
$body_crear2 = @{
  nombre = "María López"
  correo = "maria@example.com"
  mensaje = "¿Cómo me registro?"
} | ConvertTo-Json

Write-Host "`n3. POST /api/contactos - Crear segundo contacto" -ForegroundColor Green
$r3 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos" -Method POST -Body $body_crear2 -ContentType "application/json"
$r3.StatusCode
Start-Sleep -Milliseconds 500


# 4. POST - Crear tercer contacto
$body_crear3 = @{
  nombre = "Juan Pérez"
  correo = "juan@example.com"
  mensaje = "Necesito información del programa"
} | ConvertTo-Json

Write-Host "`n4. POST /api/contactos - Crear tercer contacto" -ForegroundColor Green
$r4 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos" -Method POST -Body $body_crear3 -ContentType "application/json"
$r4.StatusCode
Start-Sleep -Milliseconds 500


# 5. GET - Obtener todos (ahora debe haber 3)
Write-Host "`n5. GET /api/contactos - Verificar total" -ForegroundColor Green
$r5 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos" -Method GET
$datos5 = $r5.Content | ConvertFrom-Json
Write-Host "Total contactos: $($datos5.total)"
Start-Sleep -Milliseconds 500


# 6. GET - Obtener un contacto específico (ID=1)
Write-Host "`n6. GET /api/contactos/1 - Obtener contacto por ID" -ForegroundColor Green
$r6 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos/1" -Method GET
$r6.StatusCode
Start-Sleep -Milliseconds 500


# 7. PUT - Actualizar un contacto
$body_actualizar = @{
  nombre = "Carlos García ACTUALIZADO"
  correo = "carlos_nuevo@example.com"
  mensaje = "Mi consulta fue actualizada"
} | ConvertTo-Json

Write-Host "`n7. PUT /api/contactos/1 - Actualizar contacto" -ForegroundColor Green
$r7 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos/1" -Method PUT -Body $body_actualizar -ContentType "application/json"
$r7.StatusCode
Start-Sleep -Milliseconds 500


# 8. GET - Verificar actualización
Write-Host "`n8. GET /api/contactos/1 - Verificar que fue actualizado" -ForegroundColor Green
$r8 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos/1" -Method GET
$datos8 = $r8.Content | ConvertFrom-Json
Write-Host "Nombre actualizado: $($datos8.data.nombre)"
Start-Sleep -Milliseconds 500


# 9. DELETE - Eliminar un contacto
Write-Host "`n9. DELETE /api/contactos/2 - Eliminar contacto" -ForegroundColor Green
$r9 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos/2" -Method DELETE
$r9.StatusCode
Start-Sleep -Milliseconds 500


# 10. GET - Verificar que fue eliminado
Write-Host "`n10. GET /api/contactos - Verificar total después de eliminar" -ForegroundColor Green
$r10 = Invoke-WebRequest -Uri "http://localhost:5000/api/contactos" -Method GET
$datos10 = $r10.Content | ConvertFrom-Json
Write-Host "Total final: $($datos10.total)"


Write-Host "`n✅ PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "Resumen:" -ForegroundColor Yellow
Write-Host "✓ Creados 3 contactos"
Write-Host "✓ Actualizado 1 contacto"
Write-Host "✓ Eliminado 1 contacto"
Write-Host "✓ Total actual: $($datos10.total)"
