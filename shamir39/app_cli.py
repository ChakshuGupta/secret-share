import argparse
import click
import os
import sys

from shamir39.shamir_shares import generate, split_shares

@click.group()
def main():
    pass


@main.command()
@click.option('--words', '-w', default=12, required=False, help="Number of words in the mnemoics. Options - [12,15,18,21,24]", show_default=True)
@click.option('--export', is_flag=True, required=False, help="Export the generated mnemonics to a file")
def gen(words, export):
    """
    Command to generate new set of BIP39 mnemonics
    """
    if words not in [12,15,18,21,24]:
        raise click.BadParameter(message="Incorrect option selected. Options available- [12,15,18,21,24]")

    new_mnemonics = generate(words)
    click.echo(new_mnemonics)

    if export:
        file_handler = open("mnemonic.txt", "w")
        file_handler.write(new_mnemonics)
        file_handler.close()


@main.command()
@click.option('--input', default='', required=False, help="Input the BIP39 mnemonics through file. [Optional]")
@click.option('-n', default=2, help="Number of splits")
@click.option('-m', default=2, help="Minimum number of shares required to recover")
@click.option('--export', type=click.Choice(["SINGLE", "MULTI"]), required=False, help="Export the generated shares to a single file or multiple files (each share in separate file)")
def split(input, m, n, export):
    """
    Split the BIP39 mnemonic into Shamir39 shares
    """
    mnemonic = ""
    if not input:
        mnemonic = click.prompt("BIP39 Mnemonics: ", type=str)
    else:
        file_handler = open(input, "r")
        mnemonic = file_handler.read()
    
    shares = split_shares(mnemonic, m, n)
    click.echo(shares)

    if export == "MULTI":
        for share in shares:
            file_handler = open("shamir-share-{}.txt".format(shares.index(share)+1), "w")
            file_handler.write(share)
            file_handler.close()
    elif export == "SINGLE":
        file_handler = open("shamir-share.txt", "w")
        for share in shares:
            file_handler.write(share)
            file_handler.write("\n")
        file_handler.close()


if __name__ == "__main__":
    main()