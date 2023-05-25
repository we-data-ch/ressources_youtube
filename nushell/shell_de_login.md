## Sauvegarde de quelques configurations

## Sauvegarder les alias dans un fichier

Cela doit se faire dans bash.

```bash
# sauvegarder les alias dans un fichier
alias >> myaliases.nu
```

## Ajouter nushell aux shells reconnus par le système

Cela doit se faire dans bash.
```bash
# Ajouter nushell aux shells reconnus par le système
echo "/home/user/.cargo/bin/nu" >> /etc/shells
```

## Création des variables d'environnement à ajouter à nushell

Cela doit se faire dans nushell.

```bash
nu
```

```bash
# Création des variables d'environnement à ajouter à nushell
$env | reject config | transpose key val | each {|r| echo $"let-env ($r.key) = '($r.val)'"} | str join (char nl) | grep -v "Closure" | grep -v "PWD" | save myenv.nu
```

## Formatage dans nushell

```bash
# Formatage des alias
open myalias.nu | str replace --all "'" "" | str replace --all "=" " = " | str replace --all " ls " " ^ls " | str replace --all " rm " " ^rm " | str replace --all " mv " " ^mv " | save -f myalias.nu
```

## Ajout de variables importantes

Ajouter ces éléments:
 
```bash
# Cette ligne va reformater le path dans myenv.nu
let-env PATH = ($env.PATH | str replace -s "[" "" | str replace -s "]" "" | split row ", " | each { |x| $"($x)/" })
```

```bash
# définit vim comme éditeur par défaut (vous pouvez prendre autre chose)
let-env EDITOR = vim
```

## Importer les configurations dans nushell

```bash
source myenv.nu
```

```bash
config nu
```

```bash
source /home/user/myenv.nu
source /home/user/myaliases.nu
```

## Dernières configurations sur bash

On va maintenant définir nushell comme le shell de login par défaut.

Cela doit se faire dans bash. Si vous êtes dans nushell, faites:

```bash
exit
```

On donne la permission de changer de shell dans le fichier /etc/pam.d/chsh .

```bash
sed -i "s/auth\s*required\s*pam_shells.so/auth sufficient pam_shells.so/" /etc/pam.d/chsh
```

Son sélectionne nushell en tant que shell de login.

```bash
# défini nushell comme shell de login
chsh -s /home/user/.cargo/bin/nu
```

Il ne reste plus qu'à quitter la session et se reconnecter pour voir la différence !
