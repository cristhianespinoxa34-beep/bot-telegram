from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

TOKEN = "8695633484:AAHwgNMi6-AsWRdNQnljlUFiDtByALUsIHI"

clientes = []

# ➕ AGREGAR CLIENTE
async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nombre = context.args[0]
        dias = int(context.args[1])
        fecha = datetime.datetime.now() + datetime.timedelta(days=dias)

        clientes.append({
            "nombre": nombre,
            "chat_id": update.effective_chat.id,
            "vencimiento": fecha
        })

        await update.message.reply_text(f"✅ {nombre} agregado hasta {fecha.date()}")

    except:
        await update.message.reply_text("❌ Uso: /agregar nombre dias")


# ❌ ELIMINAR CLIENTE
async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nombre = context.args[0]

        global clientes
        clientes = [c for c in clientes if c["nombre"] != nombre]

        await update.message.reply_text(f"🗑️ {nombre} eliminado")

    except:
        await update.message.reply_text("❌ Uso: /eliminar nombre")


# 📋 LISTA DE CLIENTES
async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not clientes:
        await update.message.reply_text("📭 No hay clientes registrados")
        return

    mensaje = "📋 Lista de clientes:\n\n"

    for c in clientes:
        fecha = c["vencimiento"].date()
        mensaje += f"👤 {c['nombre']} - vence: {fecha}\n"

    await update.message.reply_text(mensaje)


# ⏰ RECORDATORIOS AUTOMÁTICOS
async def revisar(context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.datetime.now()

    for c in clientes:
        dias = (c["vencimiento"] - ahora).days

        if dias == 1:
            await context.bot.send_message(
                c["chat_id"],
                f"⚠️ Mañana vence la cuenta de {c['nombre']}"
            )

        if dias <= 0:
            await context.bot.send_message(
                c["chat_id"],
                f"❌ Hoy venció la cuenta de {c['nombre']}"
            )


# 🚀 INICIAR BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("agregar", agregar))
app.add_handler(CommandHandler("eliminar", eliminar))
app.add_handler(CommandHandler("lista", lista))

app.job_queue.run_repeating(revisar, interval=86400, first=10)

app.run_polling()