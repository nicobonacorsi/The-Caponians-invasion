from pngmatrix import load_png8
def is_rettangolo_nero(matrice, i, j, b, h):
    for x in range(i, i + h):
        for y in range(j, j + b):
            pixel = matrice[x][y]
            if pixel != (0, 0, 0):
                return False
    return True

def trova_rettangoli_neri(matrice, b, h, distanza):
    atterraggi = False
    rettangoli = {}

    for i in range(len(matrice) - h + 1):
        for j in range(len(matrice[0]) - b + 1):
            if is_rettangolo_nero(matrice, i, j, b, h):
                vertice_superiore_sinistro = (i, j)
                vertice_superiore_destro = (i, j + b - 1)
                vertice_inferiore_sinistro = (i + h - 1, j)
                vertice_inferiore_destro = (i + h - 1, j + b - 1)

                if (vertice_superiore_sinistro[1] >= (distanza)) and (vertice_superiore_destro[1] <= (len(matrice) - distanza - 1)):
                    atterraggi = True
                    nome_rettangolo = f"rettangolo_{i}_{j}"
                    rettangoli[nome_rettangolo] = {
                        "VerticeSuperioreSinistro": vertice_superiore_sinistro,
                        "VerticeSuperioreDestro": vertice_superiore_destro,
                        "VerticeInferioreSinistro": vertice_inferiore_sinistro,
                        "VerticeInferioreDestro": vertice_inferiore_destro
                    }

    return atterraggi, rettangoli

def is_area_rettangolo_nero_sx_dx(matrice, riga_A, colonna_A, riga_B, colonna_B, colonna_D,colonna_G):
    for x in range(riga_B, riga_A + 1):
        for y in range(colonna_D, colonna_G + 1):
            pixel = matrice[x][y]
            if pixel != (0, 0, 0):
                return False
    return True


def ex(file_png, file_txt, file_out):
    def trova_coordinate(city):
        coordinate = {}

        for riga in range(len(city)):
            for colonna in range(len(city[0])):
                pixel = city[riga][colonna]

                if pixel != (0, 0, 0):
                    if pixel not in coordinate:
                        coordinate[pixel] = {'min_riga': riga, 'max_riga': riga, 'min_colonna': colonna,
                                             'max_colonna': colonna}
                    else:
                        coordinate[pixel]['min_riga'] = min(coordinate[pixel]['min_riga'], riga)
                        coordinate[pixel]['max_riga'] = max(coordinate[pixel]['max_riga'], riga)
                        coordinate[pixel]['min_colonna'] = min(coordinate[pixel]['min_colonna'], colonna)
                        coordinate[pixel]['max_colonna'] = max(coordinate[pixel]['max_colonna'], colonna)

        return coordinate



    city = load_png8(file_png)
    coordinate = trova_coordinate(city)

    with open(file_out, 'w', encoding="utf-8") as output_file:
        sorted_coordinate = sorted(coordinate.items(), key=lambda x: (-x[1]['min_riga'], x[1]['min_colonna']))

        for pixel, coords in sorted_coordinate:
            ascissa_start = coords['min_colonna']
            ordinata_start = coords['min_riga']
            lunghezza_ascissa = coords['max_colonna'] - coords['min_colonna'] + 1
            lunghezza_ordinata = coords['max_riga'] - coords['min_riga'] + 1
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]

            output_file.write(f"{ascissa_start},{ordinata_start},{lunghezza_ascissa},{lunghezza_ordinata},{r},{g},{b}\n")

    with open(file_txt, mode="rt", encoding="utf-8") as file:
        lines = file.readlines()
        tuple_list = []
        temp_numbers = []

        for line in lines:
            elements = line.split()
            numbers = [int(x) for x in elements if x.isdigit()]
            temp_numbers.extend(numbers)

            while len(temp_numbers) >= 3:
                tuple_elem = tuple(temp_numbers[:3])
                tuple_list.append(tuple_elem)
                temp_numbers = temp_numbers[3:]

    astronavi = {}

    for index, elemento in enumerate(tuple_list):
        astronavi[f'Astronave_{index + 1}'] = {'larghezza': elemento[0], 'lunghezza': elemento[1], 'distanza': elemento[2]}

    controlli = []

    for astronave in astronavi:
        b = astronavi[astronave]["larghezza"]
        h = astronavi[astronave]["lunghezza"] + (2 * astronavi[astronave]["distanza"])
        distanza = astronavi[astronave]["distanza"]
        matrice = city
        atterraggi = trova_rettangoli_neri(matrice, b, h, distanza)
        rettangoli = atterraggi[1]

        if atterraggi[0] == False:
            controlli.append(False)
            continue

        risultato_astronave = False

        if atterraggi[0] == True:
            for rettangolo in rettangoli:
                colonna_sx = rettangoli[rettangolo]["VerticeSuperioreSinistro"][1]
                riga_sx_alta = rettangoli[rettangolo]["VerticeSuperioreSinistro"][0]
                riga_sx_bassa = rettangoli[rettangolo]["VerticeInferioreSinistro"][0]
                colonna_dx = rettangoli[rettangolo]["VerticeSuperioreDestro"][1]

                riga_A = riga_sx_bassa - distanza
                colonna_A = colonna_sx
                riga_B = riga_sx_alta + distanza
                colonna_B = colonna_sx
               
                colonna_D = colonna_sx - distanza

               
                colonna_G = colonna_dx + distanza

                is_area_sx_dx_nera = is_area_rettangolo_nero_sx_dx(matrice, riga_A, colonna_A, riga_B, colonna_B, colonna_D,colonna_G)

                if is_area_sx_dx_nera :
                    risultato_astronave = True
                    break

        controlli.append(risultato_astronave)

    return controlli
