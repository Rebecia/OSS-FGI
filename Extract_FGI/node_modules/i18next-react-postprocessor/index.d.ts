import {
  Module
} from 'i18next';

declare module 'i18next-react-postprocessor' {
    type Options = Partial<{
        keepUnknownVariables: boolean
        prefix: string
        suffix: string
    }>

    class ReactPostprocessor implements Module {
        type: 'postProcessor';
        constructor(opts?: Options);
    }

    export default ReactPostprocessor;
}
