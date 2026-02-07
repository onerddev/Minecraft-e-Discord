# Bot Discord com IA Gemini

## Visão Geral
Bot Discord escrito em Python que utiliza Google Gemini AI para comandos de chat e geração de imagens. O bot está hospedado no Replit com sistema de keep-alive para funcionar 24/7.

## Recursos Principais
- **Comandos de IA**: 
  - `/chat` - Conversa com Gemini 2.5 Flash
  - `/imagem` - Geração de imagens (com filtro anti-conteúdo +18)
- **Comandos Básicos**: `/ping`, `/membros`, `/say`, `/status`
- **Moderação**: `/limpar` (requer permissões)
- **Administração**: `/configurar` (ativa/desativa comandos por servidor)

## Sistema de Permissões
- Cargos suportados com emojis: Membro 👤, Moderação 🛡, Administrador 👑, Programmer ⚡
- Sistema de controle de comandos por servidor (guild_id)
- Filtro automático para conteúdo +18 em imagens

## Configuração de Hospedagem
- **Flask Keep-Alive**: Servidor rodando na porta 5000 com endpoints:
  - `/` - Status básico ("Bot online!")
  - `/uptime` - Endpoint para monitoramento externo ("Bot está funcionando! ✅")
- **Workflow**: Configurado para executar `python main.py` automaticamente

## Dependências
- `discord.py` - Integração Discord
- `google-genai` - Nova API Gemini AI 
- `Flask` - Servidor web para keep-alive
- `threading` - Para execução paralela

## Variáveis de Ambiente Necessárias
- `DISCORD_TOKEN` - Token do bot Discord
- `GEMINI_KEY` - Chave da API Google Gemini

## Estado Atual
✅ Código criado e dependências instaladas
✅ Endpoint `/uptime` configurado para monitoramento
✅ Workflow configurado
⏳ Aguardando tokens de API do usuário para teste final

## Preferências do Usuário
- Idioma: Português
- Hospedagem com keep-alive usando endpoint `/uptime`
- Integração completa com Gemini AI para chat e imagens