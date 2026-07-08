import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='*', intents=intents, help_command=None)

SCAM_ROLE_NAME = "Scameur certif"
DATA_FILE = "scam_users.json"

scam_users = set()
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            scam_users = set(json.load(f))
    except:
        pass

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(list(scam_users), f)

# ====================== VÉRIFICATION DES ROLES ======================
def has_permission(ctx):
    allowed_roles = ["Owner", "Co owner", "staff", "Manager Shop"]
    user_roles = [role.name.lower() for role in ctx.author.roles]
    return any(role.lower() in user_roles for role in allowed_roles)

# ====================== EVENTS ======================
@bot.event
async def on_ready():
    print(f"✅ Zeys Market SCAM est connecté en tant que {bot.user}")

@bot.event
async def on_member_join(member):
    if member.id in scam_users:
        role = discord.utils.get(member.guild.roles, name=SCAM_ROLE_NAME)
        if role:
            await member.add_roles(role)

# ====================== COMMANDES ======================
@bot.command()
async def addscam(ctx, member: discord.Member = None):
    if not has_permission(ctx):
        return await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande.")
    if not member:
        return await ctx.send("❌ Mentionne une personne valide. Ex: *addscam @pseudo")
    
    role = discord.utils.get(ctx.guild.roles, name=SCAM_ROLE_NAME)
    if not role:
        return await ctx.send(f"❌ Le rôle {SCAM_ROLE_NAME} n'existe pas.")
    
    await member.add_roles(role)
    scam_users.add(member.id)
    save_data()
    await ctx.send(f"✅ {member.mention} est maintenant **Scameur certif**.")

@bot.command()
async def removescam(ctx, member: discord.Member = None):
    if not has_permission(ctx):
        return await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande.")
    if not member:
        return await ctx.send("❌ Mentionne une personne valide.")
    
    role = discord.utils.get(ctx.guild.roles, name=SCAM_ROLE_NAME)
    if role:
        await member.remove_roles(role)
    scam_users.discard(member.id)
    save_data()
    await ctx.send(f"✅ Rôle Scameur certif retiré à {member.mention}.")

# Commande Help personnalisée
@bot.command(name="help")
async def help_command(ctx):
    if not has_permission(ctx):
        return await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande.")
    
    embed = discord.Embed(
        title="🛠️ Zeys Market SCAM - Commandes",
        description="Voici les commandes disponibles avec le préfixe * :",
        color=0xff0000
    )
    embed.add_field(
        name="*addscam @user",
        value="Ajoute le rôle **Scameur certif** (persistant).",
        inline=False
    )
    embed.add_field(
        name="*removescam @user",
        value="Retire le rôle **Scameur certif**.",
        inline=False
    )
    embed.set_footer(text="Zeys Market SCAM • Développé sans limite")
    await ctx.send(embed=embed)

# ====================== LANCEMENT ======================
bot.run(os.getenv("TOKEN"))   # ← Utilise la variable d'environnement (recommandé)
