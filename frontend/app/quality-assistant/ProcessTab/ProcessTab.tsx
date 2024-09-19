"use client";

import { useEffect, useState } from "react";

import { useAssistants } from "@/lib/api/assistants/useAssistants";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { filterAndSort, updateSelectedItems } from "@/lib/helpers/table";
import { useDevice } from "@/lib/hooks/useDevice";

import ProcessLine from "./Process/ProcessLine";
import styles from "./ProcessTab.module.scss";

import { Process } from "../types/process";

const mockProcesses: Process[] = [
  {
    id: 1,
    name: "Consistency Check - Etiquette VS Fiche Dev",
    datetime: new Date().toISOString(),
    status: "pending",
    result: "",
  },
  {
    id: 2,
    name: "Difference Detection - Cahier des charges 1 VS Cahier des charges 2",
    datetime: new Date(Date.now() - 100000 * 1).toISOString(),
    status: "processing",
    result: "",
  },
  {
    id: 3,
    name: "Difference Detection - Etiquette 1 VS Etiquette 2",
    datetime: new Date(Date.now() - 80430000 * 2).toISOString(),
    status: "completed",
    result: `Dans la section "50 CREPES FINES SUCREES AU", les modifications trouvées sont :
* Coupdegal**g** a été changé en : Coupdegal**o**

Dans la section "RHUM NEGRITAO (PLIEES EN QUATRE)", les modifications trouvées sont :
* TRA**C**ITION a été changé en : TRA**D**ITION
* TRA**&** INNO**V**ATION a été changé en : TRA**a** INNO**Y**ATION
* INNO**V**ATION a été changé en : INNO**Y**ATION
* INNO**IG**N a été changé en : INNO**:O**N

Dans la section "50 Thin crêpes sweetened with rum Negrita", les modifications trouvées sont :
* cr**ê**pes a été changé en : cr**è**pes
* Negrita**g** a été changé en : Negrita**e**

Dans la section "25514 Rhum NEGRITA 50 Crêpes fines sucrées au rhum cuites, surgelées", les modifications trouvées sont :
* R**k**um a été changé en : R**h**um
* Rhum**y** a été changé en : Rhum**NEGRITA**
* NEGRITA a été changé en : (supprimé)
* Crè**ê**pes a été changé en : Crè**e**pes

Dans la section "Ingrédients", les modifications trouvées sont :
* sucre de canne 16.**6**% a été changé en : sucre de canne 16.**4**%
* rhum Negrita (colorant: E150a) 3.**7**% a été changé en : rhum Negrita (colorant: E150a) 3.**6**%

Dans la section "Ingredients", les modifications trouvées sont :
* cane sugar 16.**6**% a été changé en : cane sugar 16.**4**%
* con**c**entrated butter a été changé en : con**ç**entrated butter
* Negrita rum (colouring: E150a) 3.**7**% a été changé en : Negrita rum (colouring: E150a) 3.**6**%

Dans la section "Conseil d'utilisation", les modifications trouvées sont :
* 24 heures** _ ** a été changé en : 24 heures**.**
* cr**è**pes a été changé en : cr**é**pes
* micr**o**-ondes a été changé en : micr**c**-ondes
* BPA le 24.09.2020 a été changé en : (supprimé)

Dans la section "How to prepare the products", les modifications trouvées sont :
* 0'C-+4**°**C a été changé en : 0'C-+4**C**
* +4**°**C a été changé en : +4**C**

Dans la section "Valeur énergétique/Energy", les modifications trouvées sont :
* Valeur **e**nerg**e**tique a été changé en : Valeur **é**nerg**é**tique
* 149**7** kJ a été changé en : 149**5** kJ

Dans la section "Matières grasses totales/Fat (g)", les modifications trouvées sont :
* 11.**6** a été changé en : 11.**4**

Dans la section "Acides Gras Saturés/of which saturated fatty acids (g)", les modifications trouvées sont :
* **6**.1 a été changé en : **5**.9

Dans la section "Glucides/Carbohydrates (g)", les modifications trouvées sont :
* Giu**c**des a été changé en : Giu**ri**des
* Car**p**o**n**y**ct**ates a été changé en : Car**b**o**h**y**di**ates
* 4**8**.9 a été changé en : 4**9**.5
* 24**-**1 a été changé en : 24**.2**

Dans la section "Protéines/Proteins (g)", les modifications trouvées sont :
* Protéines**/** a été changé en : Protéines

Dans la section "Sel/Salt (g)", les modifications trouvées sont :
* 0.48**->5** a été changé en : 0.48**5**

Dans la section "A conserver à -18°C", les modifications trouvées sont :
* Fabriqué en France - Made in France a été changé en : (supprimé)

Dans la section "50 CREPES FINES SUCREES AU RHUM", les modifications trouvées sont :
* NEGRITAO**->B** a été changé en : NEGRITAO**B**
* T**R**ADITION a été changé en : T**W**ADITION
* INNOVAT**:**ON a été changé en : INNOVAT**I**ON

Dans la section "50 Crêpes fines sucrées au rhum cuites, surgelées", les modifications trouvées sont :
* cr**ê**pes a été changé en : cr**è**pes

Dans la section "BATCH", les modifications trouvées sont :
* 084**2**0 a été changé en : 116**4**1
* 1**5**:4**7** a été changé en : 1**3**:1**7**

Dans la section "A consommer de préférence avant le", les modifications trouvées sont :
* 2**4**/10/2021 a été changé en : 2**5**/10/2021
* FAB : A0 a été changé en : FAB : 4A
* 09.0 a été changé en : 1.0
* 98043 a été changé en : 980
* 255141052 a été changé en : 2551410525
* 109 a été changé en : 109
* 24.10.08 a été changé en : 24.10.1162
* 20 a été changé en : 20
* 1 (91)03164 a été changé en : 1 (91)03164-17

Dans la section "EAN No", les modifications trouvées sont :
* EAN No: 03604380255141 FAB : 00001 a été changé en : EAN No: 03604380255141

Dans la section "Poids net", les modifications trouvées sont :
* Poids net : 2750 a été changé en : Poids net : 2750

Dans la section "Net weight", les modifications trouvées sont :
* Net weight : : a été changé en : Net weight : :

Dans la section "COUP DE PATES", les modifications trouvées sont :
* COUP DE PATES a été changé en : COUP DE F PATES
* S.A.S a été changé en : S.A.S
* ZAC DU BEL AIR a été changé en : ZAC DU BEL AIR
* 14-16 AVENUE a été changé en : 14-16 AVENUE
* JOSEPH PAXTON a été changé en : JOSEPH PAXTON
* FERRIERES EN BRIE 77614 MARNE LA VALLEE CEDEX 3 a été changé en : FERRIERES EN BRIE 77614 MARNE LA VALLEE CEDEX 3`,
  },
];

const ProcessTab = (): JSX.Element => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedProcess, setSelectedProcess] = useState<Process[]>([]);
  const [allChecked, setAllChecked] = useState<boolean>(false);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Process;
    direction: "ascending" | "descending";
  }>({ key: "name", direction: "ascending" });
  const [filteredProcess, setFilteredProcess] =
    useState<Process[]>(mockProcesses);
  const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
    null
  );

  const { getTasks } = useAssistants();

  const { isMobile } = useDevice();

  useEffect(() => {
    void (async () => {
      try {
        const res = await getTasks();
        console.info(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  useEffect(() => {
    setFilteredProcess(
      filterAndSort(
        mockProcesses,
        searchQuery,
        sortConfig,
        (process) => process[sortConfig.key]
      )
    );
  }, [searchQuery, sortConfig]);

  const handleDelete = () => {
    console.info("delete");
  };

  const handleSelect = (
    process: Process,
    index: number,
    event: React.MouseEvent
  ) => {
    const newSelectedProcess = updateSelectedItems<Process>({
      item: process,
      index,
      event,
      lastSelectedIndex,
      filteredList: filteredProcess,
      selectedItems: selectedProcess,
    });
    setSelectedProcess(newSelectedProcess.selectedItems);
    setLastSelectedIndex(newSelectedProcess.lastSelectedIndex);
  };

  const handleSort = (key: keyof Process) => {
    setSortConfig((prevSortConfig) => {
      let direction: "ascending" | "descending" = "ascending";
      if (
        prevSortConfig.key === key &&
        prevSortConfig.direction === "ascending"
      ) {
        direction = "descending";
      }

      return { key, direction };
    });
  };

  return (
    <div className={styles.process_tab_wrapper}>
      <span className={styles.title}>My Results</span>
      <div className={styles.table_header}>
        <div className={styles.search}>
          <TextInput
            iconName="search"
            label="Search"
            inputValue={searchQuery}
            setInputValue={setSearchQuery}
            small={true}
          />
        </div>
        <QuivrButton
          label="Delete"
          iconName="delete"
          color="dangerous"
          disabled={selectedProcess.length === 0}
          onClick={handleDelete}
        />
      </div>
      <div>
        <div className={styles.first_line}>
          <div className={styles.left}>
            <Checkbox
              checked={allChecked}
              setChecked={(checked) => {
                setAllChecked(checked);
                setSelectedProcess(checked ? filteredProcess : []);
              }}
            />
            <div className={styles.name} onClick={() => handleSort("name")}>
              Nom
              <div className={styles.icon}>
                <Icon name="sort" size="small" color="black" />
              </div>
            </div>
          </div>
          <div className={styles.right}>
            {!isMobile && (
              <>
                <div
                  className={styles.date}
                  onClick={() => handleSort("datetime")}
                >
                  Date
                  <div className={styles.icon}>
                    <Icon name="sort" size="small" color="black" />
                  </div>
                </div>
                <div
                  className={styles.status}
                  onClick={() => handleSort("status")}
                >
                  Statut
                  <div className={styles.icon}>
                    <Icon name="sort" size="small" color="black" />
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
        <div className={styles.process_list}>
          {filteredProcess.map((process, index) => (
            <div key={process.id} className={styles.process_line}>
              <ProcessLine
                process={process}
                last={index === filteredProcess.length - 1}
                selected={selectedProcess.some(
                  (item) => item.id === process.id
                )}
                setSelected={(_selected, event) =>
                  handleSelect(process, index, event)
                }
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProcessTab;
