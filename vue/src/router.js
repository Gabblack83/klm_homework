import { createWebHashHistory, createRouter } from 'vue-router'

//import cocoHome from './components/cocoHome.vue'
//import cocoList from './components/cocoList.vue'
//import cocoBrandFocalList from './components/cocoBrandFocalList.vue'
//import cocoTerms from './components/cocoTerms.vue'
//import cocoPositiveFeedback from './components/cocoPositiveFeedback.vue'
//import CocoUpload from './components/cocoUpload.vue'
//import CocoBrandFocalMatrix from './components/cocoBrandFocalMatrix.vue'
//import CocoAdmin from './components/cocoAdmin.vue'
//import CocoVisualize from './components/cocoVisualize.vue'
//import cocoManualReload from './components/cocoManualReload.vue'
//import CocoManualStop from './components/cocoManualStop.vue'
//import CocoModelSentences from './components/cocoModelSentences.vue'
//import cocoSearch from './components/cocoSearch.vue'
//import CocoSentenceTesting from './components/cocoSentenceTesting.vue'
//import CocoDetails from './components/cocoDetails.vue'
//import CocoRiskCoverage from './components/cocoRiskCoverage.vue'
//import CocoModelResults from './components/cocoModelResults.vue'
//import CocoFeedbackDetails from './components/cocoFeedbackDetails.vue'


const routes = [
  //{ name:"home", path: '/', component: App.vue },
//  { name:"list", path: '/list', component: cocoList },
//  { name:"brandFocalFeedback", path: '/brandFocalFeedback', component: cocoBrandFocalList },
//  { name:"terms", path: '/terms', component: cocoTerms },
//  { name:"positiveFeedback", path: '/positiveFeedback', component: cocoPositiveFeedback },
//  { name:"upload", path: '/upload', component: CocoUpload },
//  { name:"brandFocals", path: '/brandFocals', component: CocoBrandFocalMatrix },
//  { name:"adminFeedback", path: '/adminFeedback', component: CocoAdmin },
//  { name:"visualize", path: '/visualize/:sr/:file/:anchor?', component: CocoVisualize },
//  { name:"manual_reload", path: '/manual_reload', component: cocoManualReload },
//  { name:"manualStop", path: '/manualStop', component: CocoManualStop },
//  { name:"modelSentences", path: '/modelSentences', component: CocoModelSentences },
//  { name:"search", path: '/search', component: cocoSearch },
//  { name:"sentenceTesting", path: '/sentenceTesting', component: CocoSentenceTesting },
//  { name:"view", path: '/view/:sr', component: CocoDetails},
//  { name:"cocoRiskCoverage", path: '/riskCoverage', component: CocoRiskCoverage },
//  { name:"modelResults", path: '/modelResults', component: CocoModelResults },
//  { name:"userFeedbackDetails", path: '/userFeedbackDetails/:feedbackId', component: CocoFeedbackDetails },
//  { name:"brandFocalFeedbackDetails", path: '/brandFocalFeedbackDetails/:feedbackId', component: CocoFeedbackDetails },
//  { name:"adminFeedbackDetails", path: '/adminFeedbackDetails/:feedbackId', component: CocoFeedbackDetails }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
    if (to.meta.title) {
      document.title = to.meta.title;
    } else {
      document.title = 'KLM Homework';
    }
    next();
  });

export default router