<template>
    <div class="overall-wrapper">
        <section class="header">
            <h1>Aviation accidents by year</h1>
        </section>
        <section class="sub-header">
            <div>
                <h5>Data points with valid location coordinates</h5>
            </div>
            <div class="header-form-wrapper">
                <b>Select Year</b>

                <div class="year-select-dropdown">
                    <BFormSelect v-model="selectedYear" :options="yearList" />
                </div>
                <div class="roll-up-button-wrapper">
                    <BButton
                        :variant="getRollUpButtonVariant"
                        :disabled="currentLevel === 'continent'"
                        @click="rollUpALevel()"
                        >Roll up to previous level
                    </BButton>
                </div>
            </div>
        </section>

        <section class="data-wrapper">
            <div class="continent-level-data-wrapper" v-if="data">
                <LMap
                    id="map"
                    :zoom="currentZoomLevel"
                    :center="currentCentroid"
                    style="height: 500px; width: 45vw"
                >
                    <LTileLayer :url="tileUrl" id="mapTile" />
                    <div id="dummyClickTarget"></div>
                    <LMarker
                        v-for="(item, index) in data"
                        :key="index"
                        :lat-lng="[item['latitude'], item['longitude']]"
                    >
                        <LPopup v-if="currentLevel === 'detail'">
                            <p>
                                <b>Accident/Incident Date:</b>
                                {{ item["date"] }}
                            </p>
                            <p><b>Location:</b> {{ item["location"] }}</p>
                            <p>
                                <b>Aircraft Type:</b>
                                {{ item["aircraftModel"] }}
                            </p>
                            <p>
                                <b>Fatal:</b>
                                {{ item["totalFatalities"] > 0 ? "Yes" : "No" }}
                            </p>
                        </LPopup>
                        <LPopup v-else>
                            <p>
                                <b>{{ getCapitalizedLevelName }}:</b>
                                {{ item[`${currentLevel}Name`] }}
                            </p>
                            <p>
                                <b>Total crashes / incidents:</b>
                                {{ item["totalIncidentCount"] }}
                            </p>
                            <div class="popup-button">
                                <BButton
                                    variant="primary"
                                    size="sm"
                                    @click="drillDownALevel(item)"
                                    >See details
                                </BButton>
                            </div>
                        </LPopup>
                    </LMarker>
                </LMap>
                <BPopover
                    target="map"
                    placement="bottom-end"
                    v-if="currentLevel !== 'detail'"
                >
                    <template #title>How to use the map?</template>
                    Click on the marker to see location details and click on the
                    'See details' button to drill down to a more detailed layer
                </BPopover>
                <b-table
                    id="table"
                    striped
                    hover
                    :items="data"
                    :fields="tableFields"
                    class="table-class"
                    selectable="true"
                    sortable="true"
                    responsive="true"
                    sticky-header="true"
                    select-mode="single"
                    @row-selected="drillDownALevel"
                >
                </b-table>
                <BPopover
                    target="table"
                    placement="bottom-end"
                    v-if="currentLevel !== 'detail'"
                >
                    <template #title>How to use the table?</template>
                    Click on a row to drill down to a more detailed layer
                </BPopover>
            </div>
        </section>
    </div>
</template>

<script>
import { BButton, BFormSelect, BPopover, BTable } from "bootstrap-vue-next";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import { APICall } from "@/helpers/common";
import { nextTick } from "vue";

export default {
    name: "App",
    components: {
        BFormSelect,
        BTable,
        BButton,
        BPopover,
        LMap,
        LTileLayer,
        LMarker,
        LPopup,
    },
    data() {
        return {
            tileUrl: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            yearList: null,
            selectedYear: 2019,
            data: null,
            loading: false,
            continent: null,
            previousCentoid: null,
            currentCentroid: [0.0, -10.0],
            currentZoomLevel: 1,
            currentLevel: "continent",
            tableFields: this.turnTableFieldsToSortable([
                "continentName",
                "totalIncidentCount",
                "totalFatalities",
                "totalSeriousInjuries",
                "totalMinorInjuries",
                "totalUninjured",
            ]),
        };
    },
    methods: {
        async loadYearList() {
            this.loading = true;
            const yearListData = await APICall("/api/get_year_list");
            const yearList = [];
            yearListData["yearList"].forEach((e) => {
                yearList.push({ value: e, text: e });
            });
            this.yearList = yearList;
            this.loading = false;
        },
        async loadContinentLevelData() {
            this.loading = true;
            this.data = await APICall(
                `/api/get_continent_level_aggregation/?year=${this.selectedYear}`
            );
            this.currentCentroid = [0.0, -10.0];
            setTimeout(() => {
                this.currentZoomLevel = 1;
            }, "300");
            this.currentLevel = "continent";
            this.tableFields = this.turnTableFieldsToSortable([
                "continentName",
                "totalIncidentCount",
                "totalFatalities",
                "totalSeriousInjuries",
                "totalMinorInjuries",
                "totalUninjured",
            ]);
            this.loading = false;
        },

        async drillDownALevel(data) {
            if (this.currentLevel !== "detail") {
                this.loading = true;
                const attributes = this.getNextLevelAttributes(
                    this.currentLevel,
                    data
                );
                this.data = await APICall(attributes.apiToCall);
                this.tableFields = this.turnTableFieldsToSortable(
                    attributes.tableFields
                );
                nextTick(() => {
                    this.currentCentroid = [data.latitude, data.longitude];
                });
                // Timeout is necessary, as it has to wait until Leaflet rerenders otherwise
                // it defaults back to the former centroid.
                setTimeout(() => {
                    this.currentZoomLevel = attributes.zoomLevel;
                }, "300");
                this.simulateAClickOnMap();
                this.currentLevel = attributes.nextLevel;
                this.loading = false;
            }
        },
        getNextLevelAttributes(currentLevel, eventData) {
            const attributes = {};
            if (currentLevel === "continent") {
                attributes[
                    "apiToCall"
                ] = `/api/get_country_level_aggregation/?year=${this.selectedYear}&continent=${eventData.continentName}`;
                attributes["tableFields"] = [
                    "countryName",
                    "totalIncidentCount",
                    "totalFatalities",
                    "totalSeriousInjuries",
                    "totalMinorInjuries",
                    "totalUninjured",
                ];
                attributes["zoomLevel"] = 3;
                attributes["nextLevel"] = "country";
                this.continent = eventData.continentName;
                this.previousCentoid = [
                    eventData.latitude,
                    eventData.longitude,
                ];
            } else {
                attributes[
                    "apiToCall"
                ] = `/api/get_detail_level/?year=${this.selectedYear}&country=${eventData.countryName}`;
                attributes["tableFields"] = [
                    "date",
                    "location",
                    "aircraftModel",
                    "totalFatalities",
                    "totalSeriousInjuries",
                    "totalMinorInjuries",
                    "totalUninjured",
                ];
                attributes["zoomLevel"] = 4;
                attributes["nextLevel"] = "detail";
            }
            return attributes;
        },
        turnTableFieldsToSortable(tableFields) {
            const sortableTableFields = [];
            tableFields.forEach((e) => {
                sortableTableFields.push({
                    key: e,
                    sortable: true,
                });
            });
            return sortableTableFields;
        },
        async rollUpALevel() {
            if (this.currentLevel !== "continent") {
                this.loading = true;
                const attributes = this.getPreviousLevelAttributes(
                    this.currentLevel,
                    this.data
                );
                this.data = await APICall(attributes.apiToCall);
                this.tableFields = this.turnTableFieldsToSortable(
                    attributes.tableFields
                );
                nextTick(() => {
                    this.currentCentroid = attributes.centroid;
                });
                // Timeout is necessary, as it has to wait until Leaflet rerenders otherwise
                // it defaults back to the former centroid.
                setTimeout(() => {
                    this.currentZoomLevel = attributes.zoomLevel;
                }, "300");
                this.simulateAClickOnMap();
                this.currentLevel = attributes.nextLevel;
                this.loading = false;
            }
        },
        getPreviousLevelAttributes(currentLevel) {
            const attributes = {};
            if (currentLevel === "detail") {
                attributes[
                    "apiToCall"
                ] = `/api/get_country_level_aggregation/?year=${this.selectedYear}&continent=${this.continent}`;
                attributes["tableFields"] = [
                    "countryName",
                    "totalIncidentCount",
                    "totalFatalities",
                    "totalSeriousInjuries",
                    "totalMinorInjuries",
                    "totalUninjured",
                ];
                attributes["zoomLevel"] = 3;
                attributes["nextLevel"] = "country";
                attributes["centroid"] = this.previousCentoid;
            } else {
                attributes[
                    "apiToCall"
                ] = `/api/get_continent_level_aggregation/?year=${this.selectedYear}`;
                attributes["tableFields"] = [
                    "continentName",
                    "totalIncidentCount",
                    "totalFatalities",
                    "totalSeriousInjuries",
                    "totalMinorInjuries",
                    "totalUninjured",
                ];
                attributes["zoomLevel"] = 1;
                attributes["nextLevel"] = "continent";
                attributes["centroid"] = [0.0, -10.0];
            }
            return attributes;
        },
        simulateAClickOnMap() {
            /* Sometimes the popup remains open after drill-level transition. To deal with this 
            a mouse-click is simulated on the rerendered map. The click collapses the popup. 
            A timeout is necessary to wait for the map to get rendered */
            setTimeout(() => {
                const element = document.getElementById("dummyClickTarget");
                element.click();
            }, "500");
        },
    },
    computed: {
        getCapitalizedLevelName() {
            return (
                String(this.currentLevel).charAt(0).toUpperCase() +
                String(this.currentLevel).slice(1)
            );
        },
        getRollUpButtonVariant() {
            return this.currentLevel === "continent" ? "secondary" : "primary";
        },
    },
    async created() {
        await this.loadYearList();
        await this.loadContinentLevelData();
    },
    watch: {
        selectedYear: {
            async handler() {
                await this.loadContinentLevelData();
            },
        },
    },
};
</script>

<style scoped>
.overall-wrapper {
    background-color: #ecf3f8;
    height: 100vh;
}
.header h1 {
    margin: 20px auto auto 30px;
}
.sub-header {
    display: flex;
    justify-content: space-between;
    margin: 20px 30px 20px 30px;
}
.sub-header h5 {
    color: #00a1e4;
}
.header-form-wrapper {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-left: 20vw;
}
.year-select-dropdown {
    margin-left: 2rem;
    min-width: 10vw;
}
.data-wrapper {
    margin: 20px 30px 20px 30px;
}
.year-list-selector-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}
.year-list-selector {
    width: 20vw;
}
.roll-up-button-wrapper {
    margin-left: 2rem;
}
.continent-level-data-wrapper {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}
.popup-button {
    display: flex;
    justify-content: center;
}
.table-class {
    width: 45vw;
    height: 500px;
    max-height: 500px;
    font-size: 12px;
}
.btn-primary {
    --bs-btn-bg: #00a1e4;
    --bs-btn-border-color: #00a1e4;
}
</style>
