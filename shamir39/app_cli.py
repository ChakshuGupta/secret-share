import argparse
import click
import os
import os.path
import sys

from shamir39.shamir_shares import generate, split_shares, combine_shares, Encoding

@click.group()
def main():
    pass


@main.command()
@click.option('--words', '-w', default=12, required=False, 
                help="Number of words in the mnemoics. Options - [12,15,18,21,24]", show_default=True)
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
@click.option('--input-type', '-i', type=click.Choice(["CMD", "FILE"]), default='CMD', required=True,\
                 help="Choose the input format for the BIP39 mnemonics - file or command line.", show_default=True)
@click.option('-n', default=2, help="Number of splits")
@click.option('-m', default=2, help="Minimum number of shares required to recover")
@click.option('--encoding', default=Encoding.BIP39, help="Give flag to switch to BASE58 encoding of shares. Eg. -e 1", required=False, show_default=True)
@click.option('--export', type=click.Choice(["SINGLE", "MULTI"]), required=False,\
                help="Export the generated shares to a single file or multiple files (each share in separate file)")
def split(input_type, m, n, encoding, export):
    """
    Split the BIP39 mnemonic into Shamir39 shares
    """
    mnemonic = ""
    if input_type == "CMD":
        mnemonic = click.prompt("BIP39 Mnemonics: ", type=str)
    elif input_type == "FILE":
        file_path = click.prompt("Input File Path: ", type=str)
        if os.path.isfile(file_path):
            file_handler = open(file_path, "r")
            mnemonic = file_handler.read()
        else:
            raise click.FileError("File doesn't exist.")
    
    shares = split_shares(mnemonic, m, n, encoding)
    click.echo(shares)

    if export == "MULTI":
        for share in shares:
            file_handler = open("shamir-share-{}.txt".format(shares.index(share)+1), "w")
            file_handler.write(share)
            file_handler.close()
    else:
        file_handler = open("shamir-share.txt", "w")
        for share in shares:
            file_handler.write(share)
            file_handler.write("\n")
        file_handler.close()


@main.command()
@click.option('--input-file', '-i', nargs=2,type=(click.Choice(["SINGLE", "MULTI"]), str), required=True,\
                 help="Choose the method to input the shares for recovery. With SINGLE give FILEPATH, with MULTI give DIR_PATH")
@click.option('--encoding', default=Encoding.BIP39, help="Give flag to switch to BASE58 encoding for recovery. Eg. -e 1", required=False, show_default=True)
def recover(input_file, encoding):
    """
    Recover the private key from the given shares.
    """
    shamir_shares = list()
    if input_file[0] == "SINGLE":
        file_path = input_file[1]
        # Check if file exists
        if os.path.isfile(file_path):
            file_handler = open(file_path, "r")
            for line in file_handler:
                line = line.strip()
                if line != "":
                    shamir_shares.append(line)
        else:
            raise click.FileError("File doesn't exist.")
    else:
        dir_path = input_file[1]
        if os.path.isdir(dir_path):
            file_list = os.listdir(dir_path)
            # Iterate through the files in the directory
            for share_file in file_list:
                # Check for the file format
                if os.path.splitext(share_file)[1] == ".txt":
                    file_path = os.path.join(dir_path, share_file)
                    file_handler = open(file_path, "r")
                    for line in file_handler:
                        line = line.strip()
                        if line != "":
                            shamir_shares.append(line)
                else:
                    raise click.FileError("Incorrect file format!")
        else:
            raise click.BadParameter("Directory doesn't exist!")

    
    recovered_key = combine_shares(shamir_shares, encoding)
    click.echo(recovered_key)


if __name__ == "__main__":
    main()