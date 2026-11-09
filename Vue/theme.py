import tkinter as tk

FOND = '#0B1220'
PANNEAU = '#162338'
CARTE = '#1D3049'
TEXTE = '#F1F6FF'
SECONDAIRE = '#A6B8CD'
ACCENT = '#29B6A6'
ACCENT_SURVOL = '#38CFBB'
BORDURE = '#2C4461'


def appliquer_style(fenetre):
    fenetre.configure(bg=FOND)
    for enfant in fenetre.winfo_children():
        _style_widget(enfant)


def _style_widget(widget):
    if isinstance(widget, (tk.Toplevel, tk.Tk)):
        widget.configure(bg=FOND)
    elif isinstance(widget, tk.Button):
        texte = str(widget.cget('text')).lower()
        secondaire = any(mot in texte for mot in ('annuler', 'quitter', 'retour', 'fermer', 'non', 'actualiser'))
        fond = CARTE if secondaire else ACCENT
        avant = TEXTE if secondaire else FOND
        survol = BORDURE if secondaire else ACCENT_SURVOL
        widget.configure(bg=fond, fg=avant, activebackground=survol,
                         activeforeground=avant, relief='flat', bd=0,
                         cursor='hand2', font=('Segoe UI', 10, 'bold'),
                         padx=10, pady=7, highlightthickness=0)
    elif isinstance(widget, tk.Label):
        police = widget.cget('font')
        taille = 11
        try:
            import tkinter.font as tkfont
            taille = abs(tkfont.Font(font=police).cget('size'))
        except (tk.TclError, ValueError):
            pass
        widget.configure(bg=FOND, fg=TEXTE if taille >= 17 else SECONDAIRE,
                         font=('Segoe UI', max(10, taille), 'bold' if taille >= 17 else 'normal'))
    elif isinstance(widget, tk.Entry):
        widget.configure(bg=PANNEAU, fg=TEXTE, insertbackground=TEXTE,
                         relief='flat', bd=0, highlightthickness=1,
                         highlightbackground=BORDURE, highlightcolor=ACCENT,
                         font=('Segoe UI', 11))
    elif isinstance(widget, tk.Listbox):
        widget.configure(bg=PANNEAU, fg=TEXTE, selectbackground=ACCENT,
                         selectforeground=FOND, relief='flat', bd=0,
                         highlightthickness=0)
    elif isinstance(widget, tk.Text):
        widget.configure(bg=PANNEAU, fg=TEXTE, insertbackground=TEXTE,
                         selectbackground=CARTE, relief='flat', bd=0)
    elif isinstance(widget, tk.Menubutton):
        widget.configure(bg=CARTE, fg=TEXTE, activebackground=BORDURE,
                         activeforeground=TEXTE, relief='flat', bd=0,
                         highlightthickness=0, font=('Segoe UI', 10), padx=8, pady=5)
    elif isinstance(widget, tk.Frame):
        widget.configure(bg=FOND)
    elif isinstance(widget, tk.Scrollbar):
        widget.configure(bg=PANNEAU, activebackground=ACCENT,
                         troughcolor=FOND, highlightthickness=0, bd=0)
    for enfant in widget.winfo_children():
        if isinstance(widget, tk.Menubutton) and isinstance(enfant, tk.Menu):
            continue
        _style_widget(enfant)
