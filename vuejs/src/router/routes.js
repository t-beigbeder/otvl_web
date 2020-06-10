import TechnicalError from 'src/pages/TechnicalError'
import PageNotFoundError from 'src/pages/PageNotFoundError'

const routes = [
]

routes.push(
  {
    path: '/statics/error/technical_error.html',
    redirect: '/err'
  },
  {
    path: '/statics/error/page_not_found.html',
    redirect: '/404'
  },
  {
    path: '/err',
    component: TechnicalError
  },
  {
    path: '/404',
    component: PageNotFoundError
  }
)

export default routes
